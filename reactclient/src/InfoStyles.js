import styled from 'styled-components';
import { Card } from '@blueprintjs/core';

const InformationCard = styled(Card)`
`;

const TitleText = styled.h3`
    margin-bottom: 2px;
    margin-top: 0;
`;

const ObjectText = styled.p`
    font-size: 12px;
    font-style: italic;
`;

const Row = styled.div`
  display: flex;
  flex-wrap: wrap;
`;

const SquareImg = styled.img`
    height: 100px;
    margin-top: 10px;
`;

export {
    TitleText,
    ObjectText,
    Row,
    SquareImg,
    InformationCard,
};