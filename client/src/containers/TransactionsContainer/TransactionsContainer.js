import React, { useState, useEffect } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import Transaction from '../../components/Transaction';

const getData = (cb) => {
    console.log('GET Transactions');
    fetch('http://localhost:5000/transactions/', {mode: 'cors'})
        .then(response => response.json())
        .then(
            data => {
                console.log("Transactions received!");
                const arrData = Object.keys(data).map(i => data[i])
                cb(arrData);
            }
        ).catch(()=> {
            console.log("Error: Retrying in 10 seconds.");
            setTimeout(()=>getData(),10*1000)

        }
    );
}

const TransactionsContainer = () => {
    const [loading, setLoading] = useState(true);
    const [transactions, setTransactions] = useState([]);  

    useEffect(() => {
        getData((transactions)=>{
            console.log("getData returns: ", transactions );
            setTransactions(transactions);
            setLoading(false);
        })
      }, []);

    const getTransactions = () => (
        transactions.map(transaction => (
            <Transaction key={transaction.id} transaction={transaction}></Transaction>
        ))
    )

    if (loading) {
        return (
            <div className="mainLoading">
                <CircularProgress />
            </div>
        )
    }
    return (
        <div className="main">
            {getTransactions()}
        </div>
    );
}

export default TransactionsContainer;