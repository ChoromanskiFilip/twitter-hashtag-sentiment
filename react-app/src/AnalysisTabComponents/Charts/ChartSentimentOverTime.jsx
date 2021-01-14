import React from 'react';
import { Card } from 'react-bootstrap';
import { Hint, HorizontalGridLines, LineSeries, VerticalGridLines, XAxis, XYPlot, YAxis } from 'react-vis';

class ChartSentimentOverTime extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hintValue: null
    };
  }

  formatHint = (dataPoint) => {
    let formatedDate = `${dataPoint.x.getFullYear()}-${dataPoint.x.getMonth() + 1}-${dataPoint.x.getDate()}`
    return [
      { title: 'date', value: formatedDate },
      { title: '% of positive', value: dataPoint.y.toFixed(2) }
    ]
  }

  render() {
    return (
      <div>
        {
          this.props.data ?
            <XYPlot width={700} height={400} xType='time'
              onMouseLeave={() => this.setState({ hintValue: false })}
            >
              <HorizontalGridLines style={{ stroke: '#B7E9ED' }} />
              <VerticalGridLines style={{ stroke: '#B7E9ED' }} />
              <XAxis
                title="dates"
                style={{
                  line: { stroke: '#ADDDE1' },
                  ticks: { stroke: '#ADDDE1' },
                  text: { stroke: 'none', fill: '#6b6b76', fontWeight: 600, fontSize: 12 }
                }}
              />
              <YAxis
                title="% of positive"
                style={{
                  line: { stroke: '#ADDDE1' },
                  ticks: { stroke: '#ADDDE1' },
                  text: { stroke: 'none', fill: '#6b6b76', fontWeight: 600, fontSize: 12 }
                }}
              />
              <LineSeries
                data={this.props.data}
                style={{
                  strokeLinejoin: 'round',
                  strokeWidth: 4
                }}
                onNearestXY={(value) => this.setState({ hintValue: value })}
              />
              {this.state.hintValue &&
                <Hint value={this.state.hintValue} format={(d) => this.formatHint(d)} />
              }
            </XYPlot>
            :
            <Card>
              <Card.Body>
                <Card.Text style={{ textAlign: 'center', fontSize: '1.2rem' }}>
                  Sentiment over time plot - select hashtag to show
                </Card.Text>
              </Card.Body>
            </Card>
        }
      </div>
    );
  }
}

export default ChartSentimentOverTime;