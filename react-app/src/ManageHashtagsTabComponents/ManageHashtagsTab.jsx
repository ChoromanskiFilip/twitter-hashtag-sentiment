import Button from 'react-bootstrap/Button';
import React from 'react';
import HashtagsList from './HashtagsList/HashtagsList';
import AddHashtagModal from './HashtagsList/AddHashtagModal'

class ManageHashtagsTab extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      hashtagsList: props.hashtagsList,
      showModal: false,
    };
  }

  handleOpen = () => {
    this.setState({showModal: true})
  }

  handleClose = () => {
    this.setState({showModal: false})
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
        <HashtagsList hashtagsList={this.state.hashtagsList}/>
      </div>
      </React.Fragment>
    );
  }
}

export default ManageHashtagsTab;