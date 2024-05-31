///////////////////////////////////////////////////////////////////////
/// Generator Version 2.5
///////////////////////////////////////////////////////////////////////
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Dynamic;
using System.Linq;
using System.Net.Http;
using Microsoft.Extensions.Logging;
using System.Threading;
using Natec.Workflow.Definitions;
using System.ComponentModel;
using Natec.Workflow.Models;
using Natec.Workflow;
using Natec.Workflow.Common;
using Natec.Workflow.Extensions;
using Oracle.ManagedDataAccess.Client;
using System.Threading.Tasks;
namespace Natec.Workflow.Definition_272_59
{
#region [Used Types]
#line 1 "Definition of type WorkflowParameters"
public sealed class WorkflowParameters : BaseWorkflowParameters
{
    
    public override object Clone()
    {
        WorkflowParameters result;
        result = new WorkflowParameters();
        return result;
    }
}
#line default
#line 1 "Definition of type email"
public sealed class email : ICloneable
{
    
    // 
    private string _address;
    
    // 
    [JsonProperty("address")]
    public string address
    {
        get
        {
            return this._address;
        }
        set
        {
            this._address = value;
        }
    }
    
    public object Clone()
    {
        email result;
        result = new email();
        result.address = ((string)(address.Clone()));
        return result;
    }
}
#line default
#endregion
[Description("Workflow Class")]
public sealed class WorkflowProcess : BaseWorkflowProcess, IWorkflow, IWorkflowControl, IWorkflowState
{
    
    // 
    private WorkflowTokenManager _tokenManager;
    
    // 
    private WorkflowEnvironment _workflowEnvironment;
    
    // 
    private long _instanceId;
    
    // 
    private IEnumerable<WorkflowTransition> _transitions;
    
    // 
    private ILogger _logger;
    
    // 
    private IWorkflow _parent;
    
#region [Fields]
	private WorkflowStatus _status;
	private dynamic Global;
	private Dictionary<string, object> _nodeStates;
	private object _stateLock = new object();
	private List<WorkflowItem> _nodes;
	public WorkflowParameters Parameters;
	public IWorkflowState State {get { return this; }}
	public IServiceProvider ServiceProvider {get; private set; }
	public object WorkflowInput { get { return Input;} }
	public IEnumerable<WorkflowItem> Nodes {get {return _nodes; }}
#endregion
	public email Input { get; private set;}
#region [IWorkflowState]
	public WorkflowStatus Status { get { return _status; } set { _status = value; } }
	IEnumerable<WorkflowToken> IWorkflowState.Tokens { get { return _tokenManager.AllTokens; } }
	object IWorkflowState.Parameters  { get { return Parameters; } }
	IDictionary<string, object> IWorkflowState.NodeStates { get { return _nodeStates; } }
	dynamic IWorkflowState.Global { get { return this.Global; } }
	public IDictionary<string, WorkflowPassingNodeResult> Result { get; set; }
#endregion
	public void Init(object workflowInitData)
	{
	    _checkBaseValid();

	  if(workflowInitData is email)
	        Input = workflowInitData as email;
	    else
	    if(workflowInitData is string)
	    {
	            Input = JsonConvert.DeserializeObject<email>((string)workflowInitData, new JsonSerializerSettings());
	    }
	    _tokenManager.AllTokens.First().LastResult = new WorkflowPassingNodeResultDictionary()
	    {
	        {Services.WorkflowNameService.__zero_point_entry__ , null }
	    };
/*
	    if (Input != null)
	    {
	        _tokenManager.AllTokens.First().LastResult = new WorkflowPassingNodeResultDictionary()
	        {
	            {Services.WorkflowNameService.__zero_point_entry__ , null }
	        };
	    }
*/
	}
	public void SetState(IWorkflowPersistenceState workflowState)
	{
	    _status = workflowState.Status;
	    _tokenManager = new WorkflowTokenManager(this, workflowState.Tokens);
	    foreach (var t in _tokenManager.AllTokens)
	    {
	        var exTransition = Transitions.FindTransition(t.Transition);
	        exTransition.Counter = t.Transition.Counter;
	    }
	    Parameters = workflowState.ParametersContainer.FromJson<WorkflowParameters>() ?? new WorkflowParameters();
	    Input = workflowState.WorkflowInputContainer.FromJson(this.GetType().Assembly) as email;
	    Global = workflowState.Global;
	    _nodeStates = (workflowState.NodeStates == null) ?
	        new Dictionary<string, object>() :
	        workflowState.NodeStates.ToDictionary(kvp => kvp.Key, kvp => (object)kvp.Value);
        }
	public void SetState(IWorkflowState workflowState)
	{
	    _status = workflowState.Status;
	    _tokenManager = new WorkflowTokenManager(this, workflowState.Tokens);
	    foreach (var t in _tokenManager.AllTokens)
	    {
	        var exTransition = Transitions.FindTransition(t.Transition);
	        exTransition.Counter = t.Transition.Counter;
	    }
	    if (workflowState.Parameters is ICloneable)
	    {
	        Parameters = ((ICloneable)workflowState.Parameters).Clone() as WorkflowParameters;
	    }
	    else
	    {
	        Parameters = workflowState.Parameters as WorkflowParameters;
	    }
	    Global = workflowState.Global;
	    Input = workflowState.WorkflowInput as email;
	    _nodeStates = (workflowState.NodeStates == null) ?
	        new Dictionary<string, object>() :
	        workflowState.NodeStates.ToDictionary(kvp => kvp.Key, kvp => (object)kvp.Value);
        }
	private void _initTransitions()
	{
	    _transitions = new List<WorkflowTransition>()
	    {
			new WorkflowTransition(this, "", "Activity_Get_msisdns", "Flow_1lcy9oj", ""), // <Null>->(task)retrive the Data by http
			new WorkflowTransition(this, "Activity_Get_msisdns", "Gateway_Check_Api_Result", "Flow_0onq123", ""), // (task)retrive the Data by http->(exclusiveGateway)to check result
			new WorkflowTransition(this, "Gateway_Check_Api_Result", "Event_1wi8qel", "Flow_0o131qa84", "retry with waiting 1 sec"), // (exclusiveGateway)to check result->(intermediateCatchEvent)wait(100)
			new WorkflowTransition(this, "Event_1wi8qel", "Activity_Get_msisdns", "Flow_0onq684", ""), // (intermediateCatchEvent)wait(100)->(task)retrive the Data by http
			new WorkflowTransition(this, "Gateway_Check_Api_Result", "Activity_Form_Response", "Flow_0dz75o2", ""), // (exclusiveGateway)to check result->(task)create the Result
			new WorkflowTransition(this, "Activity_Form_Response", "", "Flow_0p9zoql", ""), // (task)create the Result->BpmnEndEventNode<End>

	    };
	}
	private void _initNodes()
	{
	    _nodes = new List<WorkflowItem>();
			// Not found implementation for 'Natec.Workflow.Definitions.WorkflowNodeStartDefinition'
			// Not found implementation for 'Natec.Workflow.Definitions.WorkflowNodeStopDefinition'
			_addNode(() =>
			{
			    var CurrentTask = new WorkflowItemTaskCodeAction(this, "Activity_Get_msisdns", "retrive the Data by http");
			    var codeAction = new CodeAction()
			    {
			        Id = "Activity_Get_msisdns",
			        Name = "retrive the Data by http",
			        Invoke = (ct, Transition, o, ctx) =>
			        {
			            var CT = ct;
#line 1 "Argument assignment for argument 'Uri' for task node 'Activity_Get_msisdns/retrive the Data by http'"
						System.Uri Uri=default(System.Uri);
						try
						{
							Uri=new Uri($"https://anyapi.io/api/v1/email?email={Input.address}&apiKey=eopl60isvuor0um4nppvgoqj1d1tcpdko7a89sr6uak80ap1jme083");
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Uri' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Headers' for task node 'Activity_Get_msisdns/retrive the Data by http'"
						Dictionary<string,string> Headers=default(Dictionary<string,string>);
						try
						{
							Headers=(Dictionary<string,string>)JsonConvert.DeserializeObject<Dictionary<string,string>>($"{{\r\n  \"Content-Type\": \"application/vnd.api+json\",\r\n  \"global_unique_id\": \"6a297fcb-956e-4228-8c11-017e9bacd629\"\r\n}}");
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Headers' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Login' for task node 'Activity_Get_msisdns/retrive the Data by http'"
						System.String Login=default(System.String);
						try
						{
							Login=$"";
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Login' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Password' for task node 'Activity_Get_msisdns/retrive the Data by http'"
						System.String Password=default(System.String);
						try
						{
							Password=$"";
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Password' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Encoding' for task node 'Activity_Get_msisdns/retrive the Data by http'"
						System.String Encoding=default(System.String);
						try
						{
							Encoding=$"utf-8";
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Encoding' : {e.Message}");
						}
#line default
						var tracker = this.ServiceProvider.GetService<Diagnostic.IWorkflowTracker>();
						if (tracker != null)
						{
						    ctx.CallingArguments = new Dictionary<string, object>()
						    {
								{"Uri",Uri},
								{"Headers",Headers},
								{"Login",Login},
								{"Password",Password},
								{"Encoding",Encoding},

						    };
						    tracker.FixPassingNode(this, "PassingNode.CallingAction", ctx);
						}

#line 1 "Call action block for task node 'Activity_Get_msisdns/retrive the Data by http'"
			        try
			        {
			            var result = CodeAction_RestApi_GET(CT,CurrentTask,Transition,Uri,Headers,Login,Password,Encoding);
			            return result;
			        }
			        catch (Exception e)
			        {
			            throw new WorkflowInvokeActionException("Error while try to call action 'Activity_Get_msisdns/retrive the Data by http'", e);
			        }
#line default
			        }
			    };

			return CurrentTask.WithAction(codeAction);
			});
			_addNode(() =>
			{
			    var activity = new WorkflowItemExclusiveGateway(this, "Gateway_Check_Api_Result", "to check result");
				activity.AddTransitionCondition("Event_1wi8qel", (CT, Transition, o) =>
				{
				    #line 1 "Expression for transition 'Flow_0o131qa84/retry with waiting 1 sec' from gateway 'Gateway_Check_Api_Result/to check result' to node 'Event_1wi8qel'"
				    return ((o.Values?.FirstOrDefault()?.Result as Models.HttpResponse).StatusCode != 200) && (Transition.Counter < 1);
				    #line default
				});
				activity.AddTransition("Activity_Form_Response");

			return activity;
			});
			_addNode(() =>
			{
			    var CurrentTask = new WorkflowItemTaskCodeAction(this, "Activity_Form_Response", "create the Result");
			    var codeAction = new CodeAction()
			    {
			        Id = "Activity_Form_Response",
			        Name = "create the Result",
			        Invoke = (ct, Transition, o, ctx) =>
			        {
			            var CT = ct;
#line 1 "Argument assignment for argument 'HttpInput' for task node 'Activity_Form_Response/create the Result'"
						Models.HttpResponse HttpInput=default(Models.HttpResponse);
						try
						{
							HttpInput=WorkflowConverter.Convert<Models.HttpResponse>((o.Values?.FirstOrDefault()?.Result as Models.HttpResponse));
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'HttpInput' : {e.Message}");
						}
#line default
						var tracker = this.ServiceProvider.GetService<Diagnostic.IWorkflowTracker>();
						if (tracker != null)
						{
						    ctx.CallingArguments = new Dictionary<string, object>()
						    {
								{"HttpInput",HttpInput},

						    };
						    tracker.FixPassingNode(this, "PassingNode.CallingAction", ctx);
						}

#line 1 "Call action block for task node 'Activity_Form_Response/create the Result'"
			        try
			        {
			            var result = CodeAction_FormReport(CT,CurrentTask,Transition,HttpInput);
			            return result;
			        }
			        catch (Exception e)
			        {
			            throw new WorkflowInvokeActionException("Error while try to call action 'Activity_Form_Response/create the Result'", e);
			        }
#line default
			        }
			    };

			return CurrentTask.WithAction(codeAction);
			});
			_addNode(() =>
			{
			    var catchEvent = new WorkflowItemIntermediateCatchEvent(this, "Event_1wi8qel", "wait(100)");
			    return catchEvent

			        .WithTimerEventDefinition(100);
			});

	}
	private void _checkBaseValid()
	{
	    if (false == _nodes?.Any())
	    throw new WorkflowValidationException($"None nodes found");
	    _transitions.CheckValid();
	}
	private void _addNode(Func<WorkflowItem> func)
	{
	    _nodes.Add(func());
	}
private static bool IsNullOrEmpty(object o)
            {
                if (o == null)
                    return true;
                else
                if (o is string)
                    return string.IsNullOrEmpty(o as string);
                else
                if (o is int)
                {
                    return (int)o == 0;
                }
                else
                if (o is float)
                {
                    return (float)o == 0;
                }
                else
                if (o is double)
                {
                    return (double)o == 0;
                }
                else
                    return true;
            }
	void IWorkflowState.Lock()
	{
	    Monitor.Enter(_stateLock);
	}
	void IWorkflowState.Unlock()
	{
	    Monitor.Exit(_stateLock);
	}
    
    public WorkflowProcess(long instanceId, IServiceProvider serviceProvider, IWorkflow parent)
    {
#region [Init]
	ServiceProvider = serviceProvider;
	_logger = ServiceProvider.GetService<ILogger>();
	_initTransitions();
	_initNodes();
	_instanceId = instanceId;
	_parent = parent;
	Parameters = new WorkflowParameters();
	Global = new ExpandoObject();
	_status = WorkflowStatus.Suspended;
	_tokenManager = new WorkflowTokenManager(this);
	_tokenManager.AddToken(_transitions.FirstTransition().GenerateToken());
	_nodeStates = new Dictionary<string, object>(StringComparer.InvariantCultureIgnoreCase);

#endregion
    }
    
    // 
    public WorkflowTokenManager TokenManager
    {
        get
        {
            return this._tokenManager;
        }
    }
    
    // 
    public WorkflowEnvironment WorkflowEnvironment
    {
        get
        {
            return this._workflowEnvironment;
        }
        set
        {
            this._workflowEnvironment = value;
        }
    }
    
    // 
    public long InstanceId
    {
        get
        {
            return this._instanceId;
        }
    }
    
    // 
    public IEnumerable<WorkflowTransition> Transitions
    {
        get
        {
            return this._transitions;
        }
    }
    
    // 
    public ILogger Logger
    {
        get
        {
            return this._logger;
        }
    }
    
    // 
    public IWorkflow Parent
    {
        get
        {
            return this._parent;
        }
    }
    
    private object CodeAction_FormReport(CancellationToken CT, WorkflowItemTaskCodeAction Action, WorkflowTransition Transition, Models.HttpResponse HttpInput)
    {
        //Common Service Funcs
        var ComeFrom = ActionServices.GetComeFromFunction(Transition);

#line 4 "Code action 'FormReport'"
//get Uri properties from http context example https://learn.microsoft.com/en-us/dotnet/api/system.uri
            var httpRequestService = ServiceProvider.GetService<HttpRequestService>();
            var httpRequest = httpRequestService.Request;
            string Query = httpRequest.Uri.Query;
            //logger using example
            Logger.LogInformation($"Uri properties from http context saved");

            //in case of arrival after retrays, it will also be default and you need to distinguish it - for example, by HTTP status code = 200
            if(HttpInput.StatusCode == 200)
            {
                var json = new JSON(HttpInput.Content);     
                bool valid = Convert.ToBoolean(json.JsonPath("$.valid").Value);                    
                Logger.LogInformation($"successful Result saved, valid result: {valid}");
                //for simplicity, we use an anonymous type with 8 properties, and .NET will automatically assign a name to it
                return new
                    {
                        Email=Input.address,
                        Query = Query,
                        Description = "Success",
                        Valid = json.JsonPath("$.validators.typo.valid").Value
                    };
            }
            else
            {
                    //for simplicity, we use an anonymous type, and .NET will automatically assign a name to it
                    Logger.LogInformation("fault Result reached");
                    
                    //change HTTP response attributes to handle error outside
                    if (WorkflowEnvironment.RuntimeName == "UCP")
                        WorkflowEnvironment.Variables["StatusCode"] = 500;
                    
                    return new
                    {
                        Email=Input.address,
                        Query = Query,
                        Description = "Fault"
                    };  
            }
#line default

    }
    
    private Models.HttpResponse CodeAction_RestApi_GET(CancellationToken CT, WorkflowItemTaskCodeAction Action, WorkflowTransition Transition, System.Uri Uri, Dictionary<string,string> Headers, string Login, string Password, string Encoding)
    {
             using (HttpClient client = new HttpClient())
            {
                using (var request = new HttpRequestMessage(HttpMethod.Get, Uri))
                {
                    try
                    {
                        string content_type = null;
                        foreach (var h in Headers)
                        {
                            if (string.Equals("Content-Type", h.Key, StringComparison.InvariantCultureIgnoreCase))
                            {
                                content_type = h.Value;
                            }
                            else
                            if (string.Equals("Accept", h.Key, StringComparison.InvariantCultureIgnoreCase))
                            {
                                request.Headers.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue(h.Value));
                            }
                            else
                            if (string.Equals("Authorization", h.Key, StringComparison.InvariantCultureIgnoreCase) &&
                                !string.IsNullOrEmpty(h.Value))
                            {
                                var prms = h.Value.Split(' ');
                                request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue(prms[0].Trim(), prms[1].Trim());
                            }
                            else
                            if (string.Equals("Content-Length", h.Key, StringComparison.InvariantCultureIgnoreCase) &&
                                !string.IsNullOrEmpty(h.Value))
                            {
                            }
                            else
                                request.Headers.Add(h.Key, h.Value);
                        }

                        if (!string.IsNullOrEmpty(Login) && !string.IsNullOrEmpty(Password))
                        {
                            var authenticationString = $"{Login}:{Password}";
                            var base64EncodedAuthenticationString =
                                Convert.ToBase64String(System.Text.ASCIIEncoding.ASCII.GetBytes(authenticationString));
                            request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", base64EncodedAuthenticationString);
                        }

                        var response = client.SendAsync(request).Result;
                        string content = response.Content.ReadAsStringAsync().Result;
                        return new Models.HttpResponse(response, content);
                    }
                    catch(Exception e)
                    {
                        Logger?.LogError($"[CallRestAPI] Error {e.Message}");
                        return new Models.HttpResponse(e);
                    }
                }
            }
    }
}
}
namespace Natec.Workflow
{
 public static class WorkflowFactory_272_59
 {
     public static IWorkflowControl CreateWorkflow(IWorkflowController controller)
     {
         return new Natec.Workflow.Definition_272_59.WorkflowProcess(controller.InstanceId, controller.ServiceProvider, null);
     }
 }
}
