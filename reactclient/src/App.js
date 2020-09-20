import React, { useState } from 'react';
import { Button, InputGroup } from "@blueprintjs/core";

import {
  VideoPlayer,
  VideoWrapper,
  SideDiv,
  MainDiv,
  InfoWindow,
  NoteWindow,
  Row,
  SaveButton,
  ExportButton,
  Setting,
} from './AppStyles';

function App() {

  const [videoID, setVideoID] = useState('');
  const [notes, setNotes] = useState('');
  const [includeLink, setIncludeLink] = useState(false);
  const [infoLoading, setInfoLoading] = useState(false);

  const defaultInfo = {
    "proper_name": null,
    "what_is_term": null,
    "description": null,
    "wikipedia_link": null,
  }

  // State variables for the fetch request
  const [data, setData] = useState(null);
  const [currentInfo, setCurrentInfo] = useState(defaultInfo);

  const validateURL = url => {
    return url.includes("youtube.com/watch?v=");
  }

  const getData = () => {
    var initialURL = document.getElementById('link').value;
    setInfoLoading(true);
    if(!validateURL(initialURL)) {
      alert('URL is not valid!');   
      return;
    }

    fetch("http://localhost:5000/getinfo?url=" + initialURL)
    .then(res => res.json())
    .then(
      (result) => {
        console.log(result);
        setInfoLoading(false);
        setData(result);
      }
    )

    initialURL = initialURL.substr(initialURL.indexOf('v=')+2);
    var id = initialURL.substr(0, initialURL.indexOf('&'));
    // console.log(id);
    setVideoID(id);
  }

  const setInfo = currentTime => {
    if(!data) return;
    var rounded = Math.round(currentTime);
    while(!(rounded.toString() in data) && rounded > 0) rounded -= 1;
    setCurrentInfo(rounded === 0 ? defaultInfo : data[rounded.toString()])
  }

  const onPlayerReady = event => {
    var player = event.target;
    player.playVideo();

    const interval = setInterval(function() {
      console.log(player.getCurrentTime());
      setInfo(player.getCurrentTime());
    }, 5000);
  }

  const onStateChange = event => {
    setInfo(event.target.getCurrentTime());
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

  function getNewNotes(notes) {
    var newNotes = notes + '\n' + currentInfo['proper_name'];
    if(currentInfo['what_is_term']) {
      newNotes += '- ' + currentInfo['what_is_term'];
    }
    if(currentInfo['description']) {
      newNotes += '\n\n' + currentInfo['description']
    }
    if(includeLink && currentInfo['wikipedia_link']) {
      newNotes += '\n\n' + currentInfo['wikipedia_link'];
    }
    newNotes += '\n'
    return newNotes;
  }

  const addToNotes = () => {
    const newNotes = getNewNotes(notes);
    document.getElementById('textArea').value = newNotes;
    setNotes(newNotes);
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
              onStateChange={onStateChange}
            />
          ) : null }
        </VideoWrapper>
        <br />
      </MainDiv>
      <SideDiv>
        <h2>Information</h2>
        <InfoWindow
          info={currentInfo}
          loading={infoLoading}
        />
        { currentInfo['proper_name'] ? (
          <Row>
            <ExportButton intent="primary" onClick={addToNotes} text="Add to Notes" />
            { currentInfo['wikipedia_link'] ? (
              <Setting checked={includeLink} onChange={() => setIncludeLink(!includeLink)} label="Include Link" />
            ): null}
          </Row>
        ) : null }
        <h2>Notes</h2>
        <NoteWindow onChange={event => {setNotes(event.target.value);}} placeholder="Take notes here!" id="textArea"></NoteWindow>
        <SaveButton onClick={saveTextAsFile} text="Save" intent="success"/>
      </SideDiv>
    </Row>
  );
}

export default App;
