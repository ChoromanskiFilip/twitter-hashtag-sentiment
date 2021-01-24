import React from 'react';
import BootstrapSwitchButton from 'bootstrap-switch-button-react'
import { Config } from 'Config';

function handleChange(checked, hashtag) {
    const requestOptions = {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'text/plain'
         },
        body: JSON.stringify({'hashtag': hashtag, 'active': checked, 'token': Config.BEARER_TOKEN})
      };
      fetch(Config.endpoints.HASHTAG_UPDATE, requestOptions)
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