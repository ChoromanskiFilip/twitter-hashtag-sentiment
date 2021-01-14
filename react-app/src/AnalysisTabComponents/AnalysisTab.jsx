import React from 'react';

import ChartsSection from './Charts/ChartsSection';
import HashtagSelector from './HashtagSelector';
import TweetsDisplayer from './TweetsDisplayer';



function AnalysisTab(props) {
  return (
    <div>
      Analysis - charts: sentiment over time (Line chart), overall sentiment (pie chart) 
      <h1>{props.selectedHashtag ? props.selectedHashtag.hashtag : ''}</h1>
      <HashtagSelector
        hashtagsList={props.hashtagsList}
        selected={props.selectedHashtag}
        setSelected={props.setSelectedHashtag}
      />
      <TweetsDisplayer tweetsList={props.exampleTweets} />
      <ChartsSection linePlotData={props.linePlotData} pieChartData={props.pieChartData}/>
    </div>
  );
}

export default AnalysisTab;