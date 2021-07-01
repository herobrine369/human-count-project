import React, {useEffect, useState} from 'react';
import axios from "axios";
import {useParams} from "react-router";
import {Link} from "react-router-dom";

const Dashboard = () => {
    let {pageNum} = useParams()
    const [totalPageNum, setTotalPageNum] = useState(1)
    const [personCountsBody, setPersonCountsBody] = useState(<></>)

    // FIXME REDIRECT NOT WORKING
    // const [redirectHead, setRedirectHead] = useState(false)
    // const [redirectTail, setRedirectTail] = useState({redirect:false, page:0})

    // constantly update the table
    useEffect(() => {
        axios.get(`persons-count/?page=${pageNum}`).then((res) => {
            let person_counts = res.data.results.map((personCount) => {
                return (
                    <tr className={"table-active"} key={personCount.time}>
                        <th className="row">
                            {personCount.time}
                        </th>
                        <td>
                            {personCount.count}
                        </td>
                    </tr>
                )
            })

            setPersonCountsBody(person_counts)
            setTotalPageNum(res.data.total_pages)

            // FIXME REDIRECT NOT WORKING
            // if (pageNum < 0) {
            //     setRedirectHead(true)
            // } else if (pageNum > totalPageNum) {
            //     setRedirectTail({redirect:true, page:totalPageNum})
            // }

            // console.log(totalPageNum)
        })
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [personCountsBody, totalPageNum])

    return (
        <div className={"container"}>

            {/*If the page number is invalid, redirect to valid page*/}
            {/*FIXME REDIRECT NOT WORKING*/}
            {/*{(()=>{*/}
            {/*    if (redirectHead){*/}
            {/*        pageNum = 1*/}
            {/*        return (<Redirect to={"/1"} />)*/}
            {/*    } else if (redirectTail.redirect) {*/}
            {/*        pageNum = redirectTail.page*/}
            {/*        return (<Redirect to={"/" + pageNum} />)*/}
            {/*    }*/}
            {/*})()}*/}

            <h3>Persons count in some place</h3>

            {/*Persons count table*/}
            <table className="table table-hover">
                <thead>
                <tr>
                    <th scope={"col"}>Time</th>
                    <th scope={"col"}>Count</th>
                </tr>
                </thead>
                <tbody>
                {personCountsBody}
                </tbody>
            </table>

            {/*pagination*/}
            <nav aria-label="Page navigation example">
                <ul className="pagination">
                    {pageNum > 1 &&
                    <li className="page-item">
                        <Link className="page-link" to={'/' + (Number.parseInt(pageNum) - 1)}>
                            Previous
                        </Link>
                    </li>}
                    {(() => {
                        let page_buttons = []
                        for (let i = 1; i <= totalPageNum; i++) {
                            page_buttons.push(
                                <li className={(i === pageNum ? "page-item" : "page-item active")} key={i}>
                                    <Link className="page-link" to={'/' + i}>
                                        {i}
                                    </Link>
                                </li>
                            )
                        }
                        return page_buttons
                    })()}
                    {pageNum < totalPageNum &&
                    <li className="page-item">
                        <Link className="page-link" to={'/' + (Number.parseInt(pageNum) + 1)}>
                            Next
                        </Link>
                    </li>}
                </ul>
            </nav>
        </div>
    );
};

export default Dashboard;
