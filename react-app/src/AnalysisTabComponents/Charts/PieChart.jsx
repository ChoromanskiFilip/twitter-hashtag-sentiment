import React from 'react';
import { Col, Row } from 'react-bootstrap';
import { DiscreteColorLegend, Hint, RadialChart } from 'react-vis';

class PieChart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hintObjTest: null
    };
  }

  formatHint = (dataPoint) => {
    let dataPointOriginal = this.props.data.find(x => x.label == dataPoint.label);
    return [
      { title: 'sentiment', value: dataPointOriginal.label },
      { title: '% of tweets', value: dataPointOriginal.angle.toFixed(2) }
    ];
  }


  render() {
    var hintObjTest = this.state.hintObjTest;
    return (
      <Row>
        <Col xs={4} style={{ marginTop: '50px', paddingRight: '5px' }}>
          <DiscreteColorLegend
            orientation='vertical'
            items={this.props.data.map(d => {
              return { title: d.label, strokeWidth: 20 };
            })}
            // @ts-ignore
            colors={this.props.data.map(d => d.color)}
          />
        </Col>
        <Col xs={8} style={{ paddingLeft: '5px' }}>
          <RadialChart
            data={this.props.data}
            radius={115}
            height={240}
            width={240}
            colorType='literal'
            onValueMouseOver={(v) => this.setState({ hintObjTest: v }) }
            onMouseLeave={() => this.setState({ hintObjTest: null }) }
          >
            {hintObjTest &&
              <Hint value={hintObjTest} format={(d) => this.formatHint(d)}/>
            }
          </RadialChart>
        </Col>
      </Row>
    );
  }
}

export default PieChart;