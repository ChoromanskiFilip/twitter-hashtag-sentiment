import React from 'react';
import FormControl from 'react-bootstrap/FormControl';
import Dropdown from 'react-bootstrap/Dropdown';

class HashtagSelector extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filteredList: null,
      open: false,
    };
  }

  componentDidUpdate() {
    if (!this.state.filteredList)
      this.setState({ filteredList: this.props.hashtagsList })
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
      filteredList: this.props.hashtagsList.filter(x =>
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
        </Dropdown.Toggle>
        {this.state.filteredList ?
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
            <div style={{ maxHeight: 180, overflowY: 'auto' }}>
              {this.state.filteredList.map((obj, i) => {
                return <Dropdown.Item key={i} onClick={() => setSelected(obj.id)}>{'#' + obj.hashtag}</Dropdown.Item>;
              })}
            </div>
          </Dropdown.Menu>
          :
          <Dropdown.Menu>
            <Dropdown.Item disabled>No data</Dropdown.Item>
          </Dropdown.Menu>
        }
      </Dropdown>
    );
  }
}

export default HashtagSelector;