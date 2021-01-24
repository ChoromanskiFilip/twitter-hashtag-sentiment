import React from 'react';
import { Modal, Button, InputGroup, FormControl } from "react-bootstrap";

class AddHashtagModal extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            newHashtag: "",
        };
    }

    handleChange = (event) => this.setState({newHashtag: event.target.value})

    render() {
        return (
            <Modal show={this.props.show} onHide={this.props.handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Adding hashtag</Modal.Title>
                </Modal.Header>
                <Modal.Body>Provide hashtag without any special characters!</Modal.Body>
                <InputGroup className="mb-1" >
                    <InputGroup.Prepend>
                        <InputGroup.Text id="basic-addon1" >#</InputGroup.Text>
                    </InputGroup.Prepend>
                    <FormControl placeholder="Hashtag" onChange={this.handleChange}/>
                </InputGroup>
                <Modal.Footer>
                    <Button variant="primary" onClick={() => this.props.handleClose(this.state.newHashtag)}> Add </Button>
                </Modal.Footer>
            </Modal>
        )
    }
}

export default AddHashtagModal;