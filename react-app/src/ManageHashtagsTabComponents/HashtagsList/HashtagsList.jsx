import React from 'react';
import Table from 'react-bootstrap/Table';
import HashtagsListRow from './HashtagsListRow';


function HashtagsList(props) {
  return (
    <div>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Hashtag</th>
            <th>Active</th>
          </tr>
        </thead>
        <tbody>
          {props.hashtagsList.map((object, i) => {
            return <HashtagsListRow row_obj={object} key={i} />;
          })}
        </tbody>
      </Table>
    </div>
  );
}

export default HashtagsList;