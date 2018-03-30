import React from 'react';

import DirectoryLayoutComponent from './directory_layout.js';
import ContentManagement from './content_management.js';

import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import Tabs, { Tab } from 'material-ui/Tabs';
import Typography from 'material-ui/Typography';

class MainScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            currentTab: 'dirlayout'
        };
        this.handleTabClick = this.handleTabClick.bind(this);
    }

    handleTabClick(event, selectedTab) {
        this.setState({ currentTab: selectedTab });
      };

    render() {
        const currentTab = this.state.currentTab;

        return (
            <React.Fragment>
            <Grid container style={{backgroundColor: '#2196f3', height: '100px', flexGrow: 1, overflow: 'hidden'}} justify="center">
                <Grid item xs={12}>
                    <Grid container justify="center" alignItems="flex-end" style={{height: '100%'}}>
                        <Grid item>
                            <Typography gutterBottom variant="headline" style={{ color: '#ffffff' }}>
                                SolarSPELL
                            </Typography>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
            <Grid container style={{overflow: 'hidden', flexGrow: 1}}>
                <Grid item xs={12}>
                    <Paper>
                        <Tabs
                            value={currentTab}
                            indicatorColor="secondary"
                            onChange={this.handleTabClick}
                            textColor="secondary"
                            centered
                        >
                            <Tab value="tags" label="Tags" />
                            <Tab value="contents" label="Content" />
                            <Tab value="dirlayout" label="Directory Layout" />
                            <Tab value="builds" label="Builds" />
                            <Tab value="sysinfo" label="System Info" />
                        </Tabs>
                    </Paper>
                </Grid>
            </Grid>
            <Grid container style={{marginTop: '20px'}}>
                <Grid item xs={12}>
                    {currentTab == 'dirlayout' && <DirectoryLayoutComponent />}
                    {currentTab == 'contents' && <ContentManagement />}
                </Grid>
            </Grid>
            </React.Fragment>
        );
    }
}

module.exports = MainScreen;
