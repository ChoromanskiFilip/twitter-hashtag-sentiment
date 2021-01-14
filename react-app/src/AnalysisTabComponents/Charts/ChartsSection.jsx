import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';

import ChartSentimentOverTime from './ChartSentimentOverTime';
import PieChart from './PieChart';



function ChartsSection(props) {
  return (
    <div>
      <Row>
        <Col>
          <h3>Percent of tweets with positive sentiment</h3>
          <ChartSentimentOverTime data={props.linePlotData} />
        </Col>
        <Col>
          <h3>Sentiment distribution</h3>
          <Container style={{marginTop: '40px'}}>
            <PieChart data={props.pieChartData} />
          </Container>
        </Col>
      </Row>
    </div>
  );
}

export default ChartsSection;