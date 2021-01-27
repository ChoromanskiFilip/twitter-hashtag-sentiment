import React from 'react';

import ChartsSection from './Charts/ChartsSection';
import HashtagSelector from './HashtagSelector';
import TweetsDisplayer from './TweetsDisplayer';
import Badge from 'react-bootstrap/Badge';



function AnalysisTab(props) {
  return (
    <div style={{ margin: '30px 0 40px 0' }}>
      <HashtagSelector
        hashtagsList={props.hashtagsList}
        selected={props.selectedHashtag}
        setSelected={props.setSelectedHashtag}
      />
      <h1 style={{ marginTop: '20px' }}>{props.selectedHashtag ? '#' + props.selectedHashtag.hashtag : ''}</h1>
      {props.dataNotCollectedYet
        ?
        <Badge variant="warning" style={{ fontSize: '1.2rem' }}>
          <div style={{ margin: '10px' }}>Data wasn't collected yet</div>
        </Badge>
        :
        <div>
          {
            props.exampleTweets ?
              <div></div>
              :
              <Badge variant="info" style={{ fontSize: '1.2rem' }}>
                <div style={{ margin: '10px' }}>Select hashtag to show statistics and additional tweets</div>
              </Badge>
          }
        </div>
      }
      <TweetsDisplayer
        tweetsList={props.exampleTweets}
        tweetsNumShow={props.tweetsNumShow}
      />
      <ChartsSection
        linePlotData={props.linePlotData}
        pieChartData={props.pieChartData}
      />
    </div>
  );
}

export default AnalysisTab;