import React from 'react';

function HashtagsListRow(props) {
    return (
        <tr>
            <td>{props.row_obj.id}</td>
            <td>{props.row_obj.hashtag}</td>
        </tr>
    );
}

export default HashtagsListRow;