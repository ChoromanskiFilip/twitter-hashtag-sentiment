import React from 'react';
import FormControl from 'react-bootstrap/FormControl';
import Dropdown from 'react-bootstrap/Dropdown';

class HashtagSelector extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filteredList: this.props.hashtagsList,
      show: false,
    };
  }

  inputWasClicked = () => {
    this._inputWasClicked = true;
  }

  onToggle = (open) => {
    if (this._inputWasClicked) {
      this._inputWasClicked = false;
      return;
    }
    this.setState({ open: open });
  }

  searchTextChanges = (searchText) => {
    this.setState({ 
      filteredList: this.props.hashtagsList.filter( x => 
        x.hashtag.toLowerCase().includes(searchText.toLowerCase())
      ) 
    });
  }

  setSelected = (id) => {
    this.props.setSelected(id);
    this._inputWasClicked = false;
  }


  render() {
    const setSelected = this.setSelected;
    return (
      <Dropdown drop='right' show={this.state.open} onToggle={this.onToggle}>
        <Dropdown.Toggle variant="success" id="dropdown-basic" style={{ width: '200px' }}  >
          Select hashtag
            {/* {props.selected ? props.selected.hashtag : "Select hashtag..."} */}
        </Dropdown.Toggle>

        <Dropdown.Menu>
          <Dropdown.Item onClick={this.inputWasClicked}>
            <FormControl
              type="text"
              autoComplete="off"
              name="search"
              placeholder="Type to filter..."
              onSelect={this.inputWasClicked}
              onChange={(e) => this.searchTextChanges(e.target.value)}
            />
          </Dropdown.Item>
          {this.state.filteredList.map((obj, i) => {
            return <Dropdown.Item key={i} onClick={() => setSelected(obj.id)}>{obj.hashtag}</Dropdown.Item>;
          })}
        </Dropdown.Menu>
      </Dropdown>
    );
  }
}

export default HashtagSelector;