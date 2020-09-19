import React, { useState } from 'react';
import { Button, InputGroup, Classes } from "@blueprintjs/core";

import {
  VideoPlayer,
  VideoWrapper,
  SideDiv,
  MainDiv,
  InfoWindow,
  NoteWindow,
  Row,
  SaveButton
} from './styles';

function App() {

  const [videoID, setVideoID] = useState('');
  const [notes, setNotes] = useState('');

  const validateURL = url => {
    if(!url.includes("youtube.com/watch?v=")) { return false; }
    return true;
  }

  const getData = () => {
    var initialURL = document.getElementById('link').value;
    if(!validateURL(initialURL)) {
      alert('URL is not valid!');
      return;
    }

    initialURL = initialURL.substr(initialURL.indexOf('v=')+2);
    var id = initialURL.substr(0, initialURL.indexOf('&'));
    console.log(id);
    setVideoID(id);
  }

  const onPlayerReady = event => {
    var player = event.target;
    player.playVideo();

    const interval = setInterval(function() {
      console.log(player.getCurrentTime());
      // Use the timestamp dictionary to change information view
    }, 5000);
  }

  const PlayButton = (
    <Button 
      large 
      text="Play" 
      intent="primary" 
      onClick={getData} 
    />
  );
  
  const saveTextAsFile = () => {
    var textFileAsBlob = new Blob([ notes ], { type: 'text/plain' });
    var fileNameToSaveAs = "notes.txt";

    var downloadLink = document.createElement("a");
    downloadLink.download = fileNameToSaveAs;
    downloadLink.innerHTML = "Download File";
    downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);

    downloadLink.click();
  }

  return (
    <Row>
      <MainDiv>
        <h2>Welcome to the Magic Zoom Bus!</h2>
        <InputGroup id="link" placeholder="Enter YouTube URL!" fill={false} rightElement={PlayButton}/>
        <VideoWrapper>
          { videoID ? (
            <VideoPlayer 
              videoId={videoID}
              onReady={onPlayerReady}
            />
          ) : null }
        </VideoWrapper>
        <br />
      </MainDiv>
      <SideDiv>
        <h2>Information</h2>
        <InfoWindow>Information</InfoWindow>
        <p>Some text about me in culpa qui officia deserunt mollit anim..</p>
        <h2>Notes</h2>
        <NoteWindow onChange={event => {setNotes(event.target.value);}} placeholder="Take notes here!" id="textArea"></NoteWindow>
        <SaveButton onClick={saveTextAsFile} text="Save" intent="success"/>
      </SideDiv>
    </Row>
  );
}

export default App;
