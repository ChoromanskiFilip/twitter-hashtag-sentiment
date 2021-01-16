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
          </tr>
        </thead>
        {props.hashtagsList ?
          <tbody>
            {props.hashtagsList.map((object, i) => {
              return <HashtagsListRow row_obj={object} key={i} />;
            })}
          </tbody>
          :
          <tbody>
            <tr><td>No data</td></tr>
          </tbody>
        }

      </Table>
    </div>
  );
}

export default HashtagsList;