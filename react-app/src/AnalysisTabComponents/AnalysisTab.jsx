import React from 'react';

import ChartsSection from './Charts/ChartsSection';
import HashtagSelector from './HashtagSelector';
import TweetsDisplayer from './TweetsDisplayer';



function AnalysisTab(props) {
  return (
    <div style={{ margin: '30px 0 40px 0' }}>
      <HashtagSelector
        hashtagsList={props.hashtagsList}
        selected={props.selectedHashtag}
        setSelected={props.setSelectedHashtag}
      />

      <h1 style={{ marginTop: '20px' }}>{props.selectedHashtag ? '#' + props.selectedHashtag.hashtag : ''}</h1>
      <TweetsDisplayer tweetsList={props.exampleTweets} tweetsNumShow={props.tweetsNumShow}/>
      <ChartsSection
        linePlotData={props.linePlotData}
        pieChartData={props.pieChartData}
      />
    </div>
  );
}

export default AnalysisTab;