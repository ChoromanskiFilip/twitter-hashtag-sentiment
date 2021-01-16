import React from 'react';
import CardDeck from 'react-bootstrap/CardDeck'
import Card from 'react-bootstrap/Card'

function TweetsDisplayer(props) {
  const tweetsNum = props.tweetsNumShow ? props.tweetsNumShow : props.tweetsList.length;
  return (
    <div style={{ margin: '30px 0px' }}>
      { props.tweetsList
        ?
        <CardDeck>
          {props.tweetsList.slice(0, tweetsNum).map((obj, i) => {
              return (
                <Card key={i} style={{ maxWidth: 400 }}>
                  <Card.Body style={{maxHeight: '300px', overflowY: 'auto'}}>
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
        <Card>
          <Card.Body>
            <Card.Text style={{ textAlign: 'center', fontSize: '1.2rem' }}>
              Example tweets - select hashtag to show
          </Card.Text>
          </Card.Body>
        </Card>
      }
    </div>
  );
}

export default TweetsDisplayer;