import axios from 'axios';
import React from 'react';

import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';

import { DIRLAYOUT_SAVE_TYPE } from './constants.js';
import { APP_URLS, get_url } from './url.js';

class DirlayoutInfoBoard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: props.boardData.id,
            name: props.boardData.name,
            description: props.boardData.description,
            fieldErrors: {}
        };
        this.handleTextFieldUpdate = this.handleTextFieldUpdate.bind(this);
        this.saveDirLayout = this.saveDirLayout.bind(this);
        this.cloneDirLayout = this.cloneDirLayout.bind(this);
        this.deleteDirLayout = this.deleteDirLayout.bind(this);
        this.saveCallback = this.props.onSave.bind(this);
        this.deleteCallback = this.props.onDelete.bind(this);
    }

    componentWillReceiveProps(props) {
        this.setState({
            id: props.boardData.id,
            name: props.boardData.name,
            description: props.boardData.description,
            fieldErrors: {}
        });
    }

    handleTextFieldUpdate(stateProperty, evt) {
        const targetVal = evt.target.value;
        this.setState((prevState, props) => {
            const newState = {
                fieldErrors: prevState.fieldErrors,
                [stateProperty]: targetVal
            };
            newState.fieldErrors[stateProperty] = null;
            return newState;
        })
    }

    saveDirLayout(evt) {
        if (!this.is_valid_state()) {
            // If it is in an invalid state, do not proceed with the save operation.
            return;
        }
        var targetUrl = APP_URLS.DIRLAYOUT_LIST;
        const payload = {name: this.state.name, description: this.state.description};
        const currentInstance = this;
        if (this.state.id > 0) {
            // Update an existing directory layout.
            targetUrl = get_url(APP_URLS.DIRLAYOUT_DETAIL, {id:this.state.id});
            axios.patch(targetUrl, payload, {
                responseType: 'json'
            }).then(function(response) {
                currentInstance.saveCallback(response.data, DIRLAYOUT_SAVE_TYPE.UPDATE);
            }).catch(function(error) {
                console.error("Error in updating the directory layout ", error);
                console.error(error.response.data);
            })
        } else {
            // Create a new directory layout.
            axios.post(targetUrl, payload, {
                responseType: 'json'
            }).then(function(response) {
                currentInstance.saveCallback(response.data, DIRLAYOUT_SAVE_TYPE.CREATE);
            }).catch(function(error) {
                console.error("Error in creating a new directory layout ", error);
                console.error(error.response.data);
            })
        }
    }

    is_valid_state() {
        var hasErrors = false;
        const fieldErrors = {};
        if (!this.state.name || this.state.name.trim().length === 0) {
            hasErrors = true;
            fieldErrors['name'] = 'Name is required.';
        }
        if (!this.state.description || this.state.description.trim().length === 0) {
            hasErrors = true;
            fieldErrors['description'] = 'Description is required.';
        }
        if (hasErrors) {
            this.setState({fieldErrors});
        }
        return !hasErrors;
    }

    cloneDirLayout(evt) {
        const targetUrl = get_url(APP_URLS.DIRLAYOUT_CLONE, {id: this.state.id});
        const currentInstance = this;
        axios.post(targetUrl, {}, {
            responseType: 'json'
        }).then(function(response) {
            currentInstance.saveCallback(response.data, DIRLAYOUT_SAVE_TYPE.CLONE);
        }).catch(function(error) {
            console.error("Error in cloning the directory layout", error);
            console.error(error.response.data);
        })
    }

    deleteDirLayout(evt) {
        // TODO : First confirm the delete action.
        const targetUrl = get_url(APP_URLS.DIRLAYOUT_DETAIL, {id:this.state.id});
        const currentInstance = this;
        axios.delete(targetUrl, {
            responseType: 'json'
        }).then(function(response) {
            currentInstance.deleteCallback(currentInstance.state.id);
        }).catch(function(error) {
            console.error("Error in deleting the directory layout ", error);
        })
    }

    render() {
        return (
            <div>
                <Button variant="raised" color="primary" onClick={this.saveDirLayout}>
                    Save
                </Button>
                {
                    this.state.id > 0 &&
                    <Button variant="raised" color="primary" onClick={this.cloneDirLayout}>
                    Clone
                    </Button>
                }
                {
                    this.state.id > 0 &&
                    <Button variant="raised" color="secondary" onClick={this.deleteDirLayout}>
                    Delete
                    </Button>
                }
                <TextField
                  id="name"
                  label="Name"
                  value={this.state.name}
                  required={true}
                  error={this.state.fieldErrors.name ? true : false}
                  onChange={evt => this.handleTextFieldUpdate('name', evt)}
                  fullWidth
                  margin="normal"
                />
                <TextField
                  id="description"
                  label="Description"
                  multiline
                  fullWidth
                  required={true}
                  error={this.state.fieldErrors.description ? true : false}
                  value={this.state.description}
                  onChange={evt => this.handleTextFieldUpdate('description', evt)}
                  margin="normal"
                />
            </div>
        );
    }
}

module.exports = DirlayoutInfoBoard;
