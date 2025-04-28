import React from 'react';
import UploadForm from './components/UploadForm';
import Player from './components/Player';
import LyricsEditor from './components/LyricsEditor';
import VideoPreview from './components/VideoPreview';
import ShareModal from './components/ShareModal';

function App() {
  return (
    <div>
      <h1>Karaoke Stem Separator</h1>
      <UploadForm />
      <Player />
      <LyricsEditor />
      <VideoPreview />
      <ShareModal />
    </div>
  );
}

export default App;
