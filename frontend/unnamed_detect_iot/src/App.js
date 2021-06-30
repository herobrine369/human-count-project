import Dashboard from "./components/Dashboard";
import {Redirect, Route, Switch} from "react-router";
import { BrowserRouter as Router } from "react-router-dom"

function App() {
    return (
        <Router>
            <Switch>
                <Route path={"/:pageNum"} children={<Dashboard/>}/>
                <Route exact path={"/"}>
                    <Redirect to={"/1"}/>
                </Route>
            </Switch>

        </Router>
    );
}

export default App;
