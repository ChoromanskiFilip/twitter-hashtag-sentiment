import React from 'react';
import CardDeck from 'react-bootstrap/CardDeck'
import Card from 'react-bootstrap/Card'

function TweetsDisplayer(props) {
  // const tweets = props.tweetsList ? this.props.tweetsList : null;
  return (
    <div style={{ margin: '40px 0px' }}>
      {props.tweetsList
        ?
        <CardDeck>
          {props.tweetsList.map((obj, i) => {
            return (
              <Card key={i} style={{  width: '20%', maxWidth: 400}}>
                <Card.Body>
                  {/* <Card.Title>Card title</Card.Title> */}
                  <Card.Text>
                    {obj.text}
                  </Card.Text>
                </Card.Body>
                <Card.Footer>
                  <small className="text-muted">Sentiment: <b>{obj.sentiment}</b></small>
                </Card.Footer>
              </Card>
            );
          })}
        </CardDeck>
        :
        <Card>No tweets</Card>
      }
    </div>
  );
}

export default TweetsDisplayer;