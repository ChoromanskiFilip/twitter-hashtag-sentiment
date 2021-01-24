import React from 'react';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';

import AnalysisTab from 'AnalysisTabComponents/AnalysisTab';
import ManageHashtagsTab from 'ManageHashtagsTabComponents/ManageHashtagsTab';

import 'App.css';
import { Config } from 'Config';


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hashtagsList: null,
      exampleTweetsList: null,
      analysisSelectedHashtag: null,
      linePlotData: null,
      pieChartData: null
    };
  }

  componentDidMount() {
    this.reload()
  }

  reload = () => {
    fetch(Config.endpoints.HASHTAGS_LIST)
    .then(res => {
      return res.json()
    })
    .then(json => this.setState({ hashtagsList: json }));
  }

  mapOverallStatistics = (stats) => {
    return [
      {
        angle: stats.tweets_negative_percent,
        count: stats.tweets_negative,
        label: 'Negative', color: '#b00404'
      },
      {
        angle: stats.tweets_positive_percent,
        count: stats.tweets_positive,
        label: 'Positive', color: '#359333'
      },
      {
        angle: stats.tweets_neutral_percent,
        count: stats.tweets_neutral,
        label: 'Neutral', color: '#c3cccf'
      }
    ]
  }

  analysisSetSelected = (id) => {
    if (this.state.analysisSelectedHashtag && id === this.state.analysisSelectedHashtag.id)
      return;
    let selectedTag = this.state.hashtagsList.find(x => x.id === id);
    fetch(Config.endpoints.HASHTAG_SUMMARY + selectedTag.hashtag)
      .then(res => res.json())
      .then(json =>
        this.setState({
          analysisSelectedHashtag: selectedTag,
          exampleTweetsList: json.sample_tweets.map(x => { return { text: x.tweet, sentiment: x.sentiment_result } }),
          linePlotData: json.daily_statistics.map(x => {
            return { x: new Date(x.date), y: x.positive_percent, tweets: x.tweets }
          }).sort((a, b) => { return new Date(a.x).getTime() - new Date(b.x).getTime() }),
          pieChartData: this.mapOverallStatistics(json.overall_statistics)
        })
      );
  }

  render() {
    return (
        <Container>
          <Tabs defaultActiveKey="analysis" id="uncontrolled-tab-example" fill className="tab-inactive">
            <Tab eventKey="analysis" title="Analysis" >
              <AnalysisTab
                hashtagsList={this.state.hashtagsList}
                selectedHashtag={this.state.analysisSelectedHashtag}
                setSelectedHashtag={this.analysisSetSelected.bind(this)}
                exampleTweets={this.state.exampleTweetsList}
                tweetsNumShow={3}
                linePlotData={this.state.linePlotData}
                pieChartData={this.state.pieChartData}
              />
            </Tab>
            <Tab eventKey="manage" title="Manage hashtags">
              <ManageHashtagsTab
                hashtagsList={this.state.hashtagsList}
                reload = {this.reload}
              />
            </Tab>
          </Tabs>
        </Container>
    );
  }
}

export default App;