import React from 'react';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';
import Container from 'react-bootstrap/Container';

import AnalysisTab from 'AnalysisTabComponents/AnalysisTab';
import ManageHashtagsTab from 'ManageHashtagsTabComponents/ManageHashtagsTab';

import 'App.css';

const MOCKhashtagsList = [
  {
    id: 1,
    hashtag: '#AndrzejDuda'
  },
  {
    id: 2,
    hashtag: '#IgaŚwiątek'
  },
  {
    id: 4,
    hashtag: '#kwarantanna'
  },
  {
    id: 7,
    hashtag: '#wośp'
  },
  {
    id: 10,
    hashtag: '#test'
  }
]

const MOCKtweetsList = [
  {
    text: "test tweets 1test tweets 1test tweets 1test tweets 1test tweets 1test tweets 1test tweets 1test tweets 1test tweets 1test tweets 1",
    sentiment: "positive"
  },
  {
    text: "test tweets 4test tweets 4test tweets 4test tweets 4",
    sentiment: "positive"
  }, {
    text: "test tweets 5test tweets 5test tweets 5test tweets 5test tweets 5test tweets 5",
    sentiment: "positive"
  },
]

const MOCKlinePlotData = [
  {
    "x": "2021-01-07",
    "y": 0.9923580288887024
  },
  {
    "x": "2021-01-08",
    "y": 0.9114131927490234
  },
  {
    "x": "2021-01-09",
    "y": 0.7338194929891162
  },
  {
    "x": "2021-01-10",
    "y": 0.5135565996170044
  },
  {
    "x": "2021-01-11",
    "y": 0.6209509753518634
  },
  {
    "x": "2021-01-12",
    "y": 0.5715724421292543
  },
  {
    "x": "2021-01-13",
    "y": 0.4079576171246435
  }
].map((obj) => {
  return {
    x: new Date(obj.x),
    y: obj.y  
  }
});

const MOCKpieChartData = [
  {angle: 11.1, label: 'Negative', color:'#b00404'}, 
  {angle: 74.23, label: 'Positive', color:'#359333'}, 
  {angle: 21.3, label: 'Neutral', color:'#c3cccf'}
]


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hashtagsList: MOCKhashtagsList,
      exampleTweetsList: MOCKtweetsList,
      analysisSelectedHashtag: null,
      linePlotData: MOCKlinePlotData,
      pieChartData: MOCKpieChartData

    };
  }

  analysisSetSelected = (id) => {
    if (this.state.analysisSelectedHashtag && id === this.state.analysisSelectedHashtag.id)
      return;
    this.setState({ analysisSelectedHashtag: this.state.hashtagsList.find(x => x.id === id) })
  }

  render() {
    return (
      <Container >
        <Tabs defaultActiveKey="analysis" id="uncontrolled-tab-example" fill className="tab-inactive">
          <Tab eventKey="analysis" title="Analysis" >
            <AnalysisTab
              hashtagsList={this.state.hashtagsList}
              selectedHashtag={this.state.analysisSelectedHashtag}
              setSelectedHashtag={this.analysisSetSelected.bind(this)}
              exampleTweets={this.state.exampleTweetsList}
              linePlotData={this.state.linePlotData}
              pieChartData={this.state.pieChartData}
            />
          </Tab>
          <Tab eventKey="manage" title="Manage hashtags">
            <ManageHashtagsTab
              hashtagsList={this.state.hashtagsList}

            />
          </Tab>
        </Tabs>
      </Container>
    );
  }
}

export default App;