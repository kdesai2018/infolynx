import styled from 'styled-components';
import YouTube from 'react-youtube';
import { Button, Checkbox } from '@blueprintjs/core';
import InfoCard from './InfoCard';


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

const InfoWindow = styled(InfoCard)`
  height: 20vh;
`;

const NoteWindow = styled.textarea`
  width: 30vw;
  resize: vertical; 
  min-height: 200px;
  max-height: 325px;
`;

const Row = styled.div`
  display: flex;
  flex-wrap: wrap;
  align-items: center;
`;

const SaveButton = styled(Button)`
  margin: 10px 2px;
`;

const ExportButton = styled(Button)`
  margin: 10px 2px;
`;

const Setting = styled(Checkbox)`
  margin: 15px 4px;
`;

const Logo = styled.img`
  height: 80px;
  width: 80px;
  position: fixed;
  top: 10px;
  right: 10px;
`;

const Title = styled.h2`
  margin-left: 10px;
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
  ExportButton,
  Setting,
  Logo,
  Title,
}