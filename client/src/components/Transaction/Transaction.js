import React, { useState } from 'react';
import "./Transaction.css";
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Grid from '@material-ui/core/Grid';

const Transaction = ( {transaction} ) => {

    const [expanded, setExpanded] = useState(false);

    const handleChange = panel => (event, isExpanded) => {
        setExpanded(isExpanded ? panel : false);
      };

    const { id, type, amount, effectiveDate } = transaction
    return (
        <ExpansionPanel expanded={expanded === 'panel'}  onChange={handleChange('panel')}>
            <ExpansionPanelSummary className={type} expandIcon={<ExpandMoreIcon />} aria-controls="panel1bh-content" id="panel1bh-header">
                <Grid container spacing={3}>
                    <Grid item xs={6}>
                        <Typography>{type}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                        <Typography>{amount}</Typography>
                    </Grid>
                </Grid>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
                
                <Grid container spacing={3}>
                    <Grid container item xs={12}>
                        <Grid item xs={6}>
                            <Typography>Transaction ID</Typography>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography>{id}</Typography>
                        </Grid>
                    </Grid>
                    <Grid container item xs={12}>
                        <Grid item xs={6}>
                            <Typography>Date</Typography>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography>{effectiveDate}</Typography>
                        </Grid>
                    </Grid>    
                </Grid>
                
            </ExpansionPanelDetails>
        </ExpansionPanel>
    )
}

export default Transaction;