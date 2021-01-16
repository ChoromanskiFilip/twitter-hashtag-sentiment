import React from 'react';
import BootstrapSwitchButton from 'bootstrap-switch-button-react'

function handleChange(checked, hashtag) {
    if (checked == false) {
        console.log(`Send API request to make hashtag ${hashtag} inactive`)
    } else {
        console.log(`Send API request to make hashtag ${hashtag} active`)
    }
}

function HashtagsListRow(props) {
    return (
        <tr>
            <td>{props.row_obj.id}</td>
            <td>#{props.row_obj.hashtag}</td>
            <td><BootstrapSwitchButton onstyle="outline-info" offstyle="outline-primary" 
                checked={props.row_obj.active} size="sm" onChange={(checked) => handleChange(checked, props.row_obj.hashtag)}/>
            </td>
        </tr>
    );
}

export default HashtagsListRow;