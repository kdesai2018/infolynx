import React from 'react';
import { Card } from '@blueprintjs/core';

import {
  TitleText,
  ObjectText,
} from './InfoStyles';

function InfoCard(props) {

  const {
    proper_name,
    what_is_term,
    description,
    wikipedia_link 
  } = props.info;  

  return (
    <Card>
        <TitleText>{proper_name}</TitleText>
        <ObjectText>{what_is_term}</ObjectText>
        <p>{description}</p>
        {wikipedia_link ? (
          <a href={wikipedia_link} target="_blank">Wikipedia</a>
        ): null}
    </Card>
  );
}

export default InfoCard;
