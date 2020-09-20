import React from 'react';
import { ProgressBar } from '@blueprintjs/core';
import {
  TitleText,
  ObjectText,
  Row,
  SquareImg,
  InformationCard,
} from './InfoStyles';

function InfoCard(props) {

  const {
    proper_name,
    what_is_term,
    description,
    wikipedia_link,
    image_url
  } = props.info;  

  const isLoading = props.loading;

  return (
    <InformationCard>
      {isLoading ? (
        <ProgressBar intent="success" />
      ) : (
        <Row>
          <div>
            <TitleText>{proper_name}</TitleText>
            <ObjectText>{what_is_term}</ObjectText>
            <p>{description}</p>
            {wikipedia_link ? (
              <>
                <a href={wikipedia_link} target="_blank">Wikipedia</a>
                <br />
              </>
            ): null}
            { image_url ? (
              <SquareImg src={image_url}/>
            ) : null }    
          </div>  
        </Row>
      )}
    </InformationCard>
  );
}

export default InfoCard;
