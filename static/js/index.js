
const URL = '/translate?q=';
let root = document.getElementById("root");
let cookie = document.cookie;
let username = "randoName";
// TODO : finish cookie generation for persistent translation history
cookie = [];

class TranslateInput extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            inputText : undefined,
            output : "Translated Inupiaq text will appear here!",
        };
    }
    render(){
        return(
			<form id='input' onSubmit={this.submitToAPI}>
				<div class="container">
				<div class="row">
					<div class="col">
						<label>English:</label>
						<textarea id='inputText' rows="5" wrap='hard' class='form-control'
							value={this.state.inputText} onChange={this.handleChange}
							placeholder={this.state.inputText === undefined ? "Enter English text here!" : ""}>
						</textarea>
					</div>
					<div class="col">
						<p> Inupiaq: </p>
						<p>{this.state.output}</p>
                        <button onClick={this.rememberTranslation}>Save Translation</button>
					</div>
				</div>
				</div>
			</form>
        );
    }
    handleChange = (event) => {
        let eventValue = event.target.value;
        this.setState({ inputText : eventValue }, () => {
            if(eventValue != ""){
                this.submitToAPI(eventValue);
            }
            else{
                this.setState({ output : "" });
            }
        });
        event.preventDefault();
    }
    submitToAPI = async (eventValue) => {
		let url = URL + eventValue;
        fetch(url)
		  .then(response => response.json())
		  .then(json => {
			this.setState({output : json });
		  })
		  .catch(err => {
			  alert("Error: " + err);
			  console.log(err)
		  });
    }
    rememberTranslation = (event) => {
        cookie.push([this.state.inputText, this.state.output]);
        console.log(cookie);
        event.preventDefault();
    }
}

ReactDOM.render(<TranslateInput />, root);
