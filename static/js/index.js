const URL = '/translate?q=';
let root = document.getElementById("root");

class TranslateInput extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            text : null,
            output : "Translated text will appear here!"
        };
    }
    render(){
        return(
			<form id='input' onSubmit={this.submitToAPI}>
				<div class="container">
				<div class="row">
					<div class="col">
						<textarea id='inputText' cols="3" rows="5" wrap='hard' class=' form-control'
							value={this.state.text} onChange={this.handleChange}
							placeholder={this.state.text === null ? "Enter text here!" : ""}>
						</textarea>
					</div>
					<div class="col">
						<p> Inupiaq: </p>
						<p>{this.state.output}</p>
					</div>
				</div>
				</div>
			</form>
        );
    }
    handleChange = (event) => {
        this.setState({
            text : event.target.value
        });
		if(event.target.value != ""){
			this.submitToAPI(event);
		}
		else{
			this.setState({ output : "" });
		}
		event.preventDefault();
    }
    submitToAPI = async (event) => {
		this.setState({ output : "" });
		let url = URL + event.target.value;
        fetch(url)
		  .then(response => response.json())
		  .then(json => {
			this.setState({output : json });
		  })
		  .catch(err => {
			  alert("Error: " + err);
			  console.log(err)
		  });
		event.preventDefault();
    }
}
ReactDOM.render(<TranslateInput />, root);
