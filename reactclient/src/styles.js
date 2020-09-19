import styled from 'styled-components';
import YouTube from 'react-youtube';
import { TextArea, Button } from '@blueprintjs/core';

const VideoPlayer = styled(YouTube)`
    height: 75vh;
    width: 100%;
`;

const VideoWrapper = styled.div`
    height: 70vh;
    margin: 10px 0;
`;

const SideDiv = styled.div`
  flex: 35%;
  background-color: #f1f1f1;
  padding: 20px;
`;

const MainDiv = styled.div`
  flex: 65%;
  background-color: white;
  padding: 20px;
`;

const InfoWindow = styled.div`
  height: 20vh;
`;

const NoteWindow = styled(TextArea)`
  width: 30vw;
  resize: vertical; 
  min-height: 225px;
  max-height: 325px;
`;

const Row = styled.div`
  display: flex;
  flex-wrap: wrap;
`;

const SaveButton = styled(Button)`
  margin: 10px 2px;
`;

export { 
  VideoPlayer, 
  VideoWrapper,
  SideDiv,
  MainDiv,
  InfoWindow,
  NoteWindow,
  Row,
  SaveButton,
}