const URL = 'http://192.168.1.139:5000/translate?q=';
let root = document.getElementById("root");

class TranslateInput extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            text : "Enter text here!",
            output : "Translated text will appear here!"
        };
    }
    render(){
        return(
            <div>
                <form id='input' onSubmit={this.submitToAPI}>
                    <textarea id='inputText' cols="50" rows="7" wrap='hard' 
						value={this.state.text} onChange={this.handleChange}></textarea>
                    <input type='submit' value='Translate'/>
                </form>
                <p> Inupiaq: </p>
                <textarea value={this.state.output} onChange={() => null}></textarea>
            </div>
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
