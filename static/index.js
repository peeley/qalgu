class TranslateInput extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            text : "Enter text here!",
            output : ""
        };
    }
    render(){
        return(
            <div>
                <form id='input' onSubmit={this.submitToAPI}>
                    <textarea id='inputText' cols="50" rows="7" wrap='hard' value={this.state.text} onChange={this.handleChange}></textarea>
                    <input type='submit' value='Translate'/>
                </form>
                <p> Inupiaq: </p>
                <p> {this.state.output} </p>
            </div>
        );
    }
    handleChange = (event) => {
        this.setState({
            text : event.target.value
        });
    }
    submitToAPI = async () => {
        fetch('localhost:5000/translate?q=' + this.state.text)
            .then((res) => {
                res.json().then((data) => {
                    alert(date);
                    this.setState({
                        output : data
                    });
                });
            })   
            .catch((err) => {
                console.log(err);
                return;
            });
    }
}
let root = document.getElementById("root");
ReactDOM.render(<TranslateInput />, root);
