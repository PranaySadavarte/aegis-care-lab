import sys,json,tempfile,unittest
from pathlib import Path
from datetime import datetime,timedelta,timezone
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'dashboard'))
from voice_session import VoiceSession

class VoiceReadiness(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);(self.root/'dashboard').mkdir();(self.root/'evidence').mkdir()
        self.voice=VoiceSession(self.root)
    def prepared(self,minutes):
        self.voice.process=Mock();self.voice.process.poll.return_value=None
        self.voice.manifest.write_text(json.dumps({'pid':999,'url':'https://app.goguava.ai/debug-webrtc?webrtc_code=synthetic','expires_at':(datetime.now(timezone.utc)+timedelta(minutes=minutes)).isoformat()}))
        self.voice.log.write_text('Started listing on WebRTC code synthetic')
    def test_saved_url_without_owned_process_is_stopped(self):
        self.prepared(30);self.voice.process=None
        self.assertEqual(self.voice.status(),{'status':'stopped'})
    def test_expired_code_never_returns_url(self):
        self.prepared(-1);self.assertEqual(self.voice.status(),{'status':'expired'})
    def test_registration_required_and_windows_child_pid_allowed(self):
        self.prepared(30);self.voice.process.pid=111
        self.assertEqual(self.voice.status()['status'],'ready')
        self.voice.log.write_text('creating temporary code')
        self.assertEqual(self.voice.status(),{'status':'starting'})
    def test_ready_start_reuses_listener_without_network(self):
        self.prepared(30)
        with patch('voice_session.subprocess.Popen') as spawn:
            self.assertEqual(self.voice.start()['status'],'ready');spawn.assert_not_called()
    def test_expired_start_removes_stale_manifest(self):
        self.prepared(-1)
        with patch('voice_session.subprocess.Popen') as spawn,patch('voice_session.subprocess.run'):
            self.assertEqual(self.voice.start(),{'status':'starting'})
            self.assertFalse(self.voice.manifest.exists());spawn.assert_called_once()
