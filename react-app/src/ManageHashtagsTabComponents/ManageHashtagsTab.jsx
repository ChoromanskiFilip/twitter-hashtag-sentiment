import Button from 'react-bootstrap/Button';
import React from 'react';
import HashtagsList from './HashtagsList/HashtagsList';
import AddHashtagModal from './HashtagsList/AddHashtagModal'
import { Config } from 'Config';

class ManageHashtagsTab extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      showModal: false,
    };
  }

  handleOpen = () => {
    this.setState({showModal: true})
  }

  handleClose = (newHashtag) => {
    this.setState({showModal: false})
    if (newHashtag == undefined) {
      return
    }
    const requestOptions = {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'text/plain'
       },
      body: JSON.stringify({ 'hashtag': newHashtag, 'token': Config.BEARER_TOKEN})
    };
    fetch(Config.endpoints.HASHTAG_ADD, requestOptions)
        .then(() => this.props.reload())
  }

  render() {
    console.log(this.state.showModal)
    return (
      <React.Fragment>
      <div>
        <AddHashtagModal show={this.state.showModal} handleClose={this.handleClose} />
        {/* ManageHashtags - hashtags list, add hashtag, - next: remove hashtags */}
        <Button style={{margin: '20px 0px'}} variant="info" block onClick={this.handleOpen}>
          Add hashtag
        </Button>
        <HashtagsList hashtagsList={this.props.hashtagsList}/>
      </div>
      </React.Fragment>
    );
  }
}

export default ManageHashtagsTab;