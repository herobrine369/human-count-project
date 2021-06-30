/* eslint-disable jsx-a11y/anchor-is-valid */
import React, {useEffect, useState} from 'react';
import axios from "axios";

const Dashboard = () => {
    const [totalPageNum, setTotalPageNum] = useState(1)
    const [pageNum, setPageNum] = useState(1)
    const [personCounts, setPersonCounts] = useState([])

    const update = () => {
        axios.get(`persons-count/?page=${pageNum}`).then((res) => {
            setPersonCounts(res.data.results)
            setTotalPageNum(res.data.total_pages)
        })
    }

    useEffect(() => {
        update()
    })

    return (
        <div className={"container"}>
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
                {personCounts.map((personCount) => {
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
                })}
                </tbody>
            </table>

            {/*pagination*/}
            <nav aria-label="Page navigation example">
                <ul className="pagination">
                    {pageNum > 1 && <li className="page-item"><a className="page-link" href="#"
                                                                 onClick={() => setPageNum(pageNum - 1)}>Previous</a>
                    </li>}
                    {(() => {
                        let page_buttons = []
                        for (let i = 1; i <= totalPageNum; i++) {
                            page_buttons.push(<li className={(i === pageNum ? "page-item" : "page-item active")}
                                                  key={i}><a className="page-link"
                                                             href="#"
                                                             onClick={() => {
                                                                 setPageNum(i)
                                                             }}>{i}</a>
                            </li>)
                        }
                        return page_buttons
                    })()}
                    {pageNum < totalPageNum && <li className="page-item"><a className="page-link" href="#"
                                                                            onClick={() => setPageNum(pageNum + 1)}>Next</a>
                    </li>}
                </ul>
            </nav>
        </div>
    );
};

export default Dashboard;
