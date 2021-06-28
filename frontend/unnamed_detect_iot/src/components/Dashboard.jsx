import React, {useEffect, useState} from 'react';
import axios from "axios";

// TODO: finish the counts of persons list
// TODO: template below:
{/*<ul className="list-group">*/}
{/*    <li className="list-group-item">*/}

{/*    </li>*/}
{/*</ul>*/}
const Dashboard = () => {
    const [body, setBody] = useState(<></>)
    useEffect(()=>{
        axios.get("persons-count/").then((res)=>{
            // res.data.map()
        })
    })

    return (
        <div>

        </div>
    );
};

export default Dashboard;