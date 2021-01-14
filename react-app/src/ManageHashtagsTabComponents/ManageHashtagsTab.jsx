import Button from 'react-bootstrap/Button';
import React from 'react';
import HashtagsList from './HashtagsList/HashtagsList';

function ManageHashtagsTab(props) {
  return (
    <div>
      {/* ManageHashtags - hashtags list, add hashtag, - next: remove hashtags */}
      <Button style={{margin: '20px 0px'}} variant="info" block >
        Add hashtag
      </Button>
      <HashtagsList hashtagsList={props.hashtagsList}/>
    </div>
  );
}

export default ManageHashtagsTab;