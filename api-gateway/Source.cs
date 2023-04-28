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
namespace Natec.Workflow.Definition_311_2
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
	public Models.HttpRequest Input { get; private set;}
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

	  if(workflowInitData is Models.HttpRequest)
	        Input = workflowInitData as Models.HttpRequest;
	    else
	    if(workflowInitData is string)
	    {
	            Input = JsonConvert.DeserializeObject<Models.HttpRequest>((string)workflowInitData, new JsonSerializerSettings());
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
	    Input = workflowState.WorkflowInputContainer.FromJson(this.GetType().Assembly) as Models.HttpRequest;
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
	    Input = workflowState.WorkflowInput as Models.HttpRequest;
	    _nodeStates = (workflowState.NodeStates == null) ?
	        new Dictionary<string, object>() :
	        workflowState.NodeStates.ToDictionary(kvp => kvp.Key, kvp => (object)kvp.Value);
        }
	private void _initTransitions()
	{
	    _transitions = new List<WorkflowTransition>()
	    {
			new WorkflowTransition(this, "", "Activity_0h5bu4y", "Flow_0p9xzvl", ""), // <Null>->(task)correct Models
			new WorkflowTransition(this, "Activity_0h5bu4y", "Activity_05w7xhk", "Flow_1hv0uey", ""), // (task)correct Models->(task)call REST API function
			new WorkflowTransition(this, "Activity_05w7xhk", "Activity_034lr3e", "Flow_1opdmgx", ""), // (task)call REST API function->(task)form Response
			new WorkflowTransition(this, "Activity_034lr3e", "", "Flow_0d6cqzk", ""), // (task)form Response->BpmnEndEventNode<End>

	    };
	}
	private void _initNodes()
	{
	    _nodes = new List<WorkflowItem>();
			// Not found implementation for 'Natec.Workflow.Definitions.WorkflowNodeStartDefinition'
			// Not found implementation for 'Natec.Workflow.Definitions.WorkflowNodeStopDefinition'
			_addNode(() =>
			{
			    var CurrentTask = new WorkflowItemTaskCodeAction(this, "Activity_0h5bu4y", "correct Models");
			    var codeAction = new CodeAction()
			    {
			        Id = "Activity_0h5bu4y",
			        Name = "correct Models",
			        Invoke = (ct, Transition, o, ctx) =>
			        {
			            var CT = ct;
#line 1 "Argument assignment for argument 'Test' for task node 'Activity_0h5bu4y/correct Models'"
						System.String Test=default(System.String);
						try
						{
							Test=$"test";
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Test' : {e.Message}");
						}
#line default
						var tracker = this.ServiceProvider.GetService<Diagnostic.IWorkflowTracker>();
						if (tracker != null)
						{
						    ctx.CallingArguments = new Dictionary<string, object>()
						    {
								{"Test",Test},

						    };
						    tracker.FixPassingNode(this, "PassingNode.CallingAction", ctx);
						}

#line 1 "Call action block for task node 'Activity_0h5bu4y/correct Models'"
			        try
			        {
			            var result = CodeAction_CorrectModels(CT,CurrentTask,Transition,Test);
			            return result;
			        }
			        catch (Exception e)
			        {
			            throw new WorkflowInvokeActionException("Error while try to call action 'Activity_0h5bu4y/correct Models'", e);
			        }
#line default
			        }
			    };

			return CurrentTask.WithAction(codeAction);
			});
			_addNode(() =>
			{
			    var CurrentTask = new WorkflowItemTaskCodeAction(this, "Activity_05w7xhk", "call REST API function");
			    var codeAction = new CodeAction()
			    {
			        Id = "Activity_05w7xhk",
			        Name = "call REST API function",
			        Invoke = (ct, Transition, o, ctx) =>
			        {
			            var CT = ct;
#line 1 "Argument assignment for argument 'Uri' for task node 'Activity_05w7xhk/call REST API function'"
						System.Uri Uri=default(System.Uri);
						try
						{
							Uri=WorkflowConverter.Convert<System.Uri>((o.Values?.FirstOrDefault()?.Result as Models.HttpRequest).Uri);
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Uri' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Method' for task node 'Activity_05w7xhk/call REST API function'"
						System.String Method=default(System.String);
						try
						{
							Method=$"POST";
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Method' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Login' for task node 'Activity_05w7xhk/call REST API function'"
						System.String Login=default(System.String);
						try
						{
							Login=$"api_user";
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Login' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Password' for task node 'Activity_05w7xhk/call REST API function'"
						System.String Password=default(System.String);
						try
						{
							Password=$"Widecoup1";
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Password' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Headers' for task node 'Activity_05w7xhk/call REST API function'"
						Dictionary<string,string> Headers=default(Dictionary<string,string>);
						try
						{
							Headers=WorkflowConverter.Convert<Dictionary<string,string>>((o.Values?.FirstOrDefault()?.Result as Models.HttpRequest).Headers);
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Headers' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Body' for task node 'Activity_05w7xhk/call REST API function'"
						System.String Body=default(System.String);
						try
						{
							Body=WorkflowConverter.Convert<System.String>((o.Values?.FirstOrDefault()?.Result as Models.HttpRequest).Content);
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Body' : {e.Message}");
						}
#line default
#line 1 "Argument assignment for argument 'Encoding' for task node 'Activity_05w7xhk/call REST API function'"
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
								{"Method",Method},
								{"Login",Login},
								{"Password",Password},
								{"Headers",Headers},
								{"Body",Body},
								{"Encoding",Encoding},

						    };
						    tracker.FixPassingNode(this, "PassingNode.CallingAction", ctx);
						}

#line 1 "Call action block for task node 'Activity_05w7xhk/call REST API function'"
			        try
			        {
			            var result = CodeAction_RestApi(CT,CurrentTask,Transition,Uri,Method,Login,Password,Headers,Body,Encoding);
			            return result;
			        }
			        catch (Exception e)
			        {
			            throw new WorkflowInvokeActionException("Error while try to call action 'Activity_05w7xhk/call REST API function'", e);
			        }
#line default
			        }
			    };

			return CurrentTask.WithAction(codeAction);
			});
			_addNode(() =>
			{
			    var CurrentTask = new WorkflowItemTaskCodeAction(this, "Activity_034lr3e", "form Response");
			    var codeAction = new CodeAction()
			    {
			        Id = "Activity_034lr3e",
			        Name = "form Response",
			        Invoke = (ct, Transition, o, ctx) =>
			        {
			            var CT = ct;
#line 1 "Argument assignment for argument 'Response' for task node 'Activity_034lr3e/form Response'"
						Models.HttpResponse Response=default(Models.HttpResponse);
						try
						{
							Response=WorkflowConverter.Convert<Models.HttpResponse>((o.Values?.FirstOrDefault()?.Result as Models.HttpResponse));
						}
						catch(Exception e)
						{
							throw new WorkflowException($"Error while try to assign argument 'Response' : {e.Message}");
						}
#line default
						var tracker = this.ServiceProvider.GetService<Diagnostic.IWorkflowTracker>();
						if (tracker != null)
						{
						    ctx.CallingArguments = new Dictionary<string, object>()
						    {
								{"Response",Response},

						    };
						    tracker.FixPassingNode(this, "PassingNode.CallingAction", ctx);
						}

#line 1 "Call action block for task node 'Activity_034lr3e/form Response'"
			        try
			        {
			            var result = CodeAction_FormResponse(CT,CurrentTask,Transition,Response);
			            return result;
			        }
			        catch (Exception e)
			        {
			            throw new WorkflowInvokeActionException("Error while try to call action 'Activity_034lr3e/form Response'", e);
			        }
#line default
			        }
			    };

			return CurrentTask.WithAction(codeAction);
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
    
    private Models.HttpRequest CodeAction_CorrectModels(CancellationToken CT, WorkflowItemTaskCodeAction Action, WorkflowTransition Transition, string Test)
    {
        //Common Service Funcs
        var ComeFrom = ActionServices.GetComeFromFunction(Transition);

#line 4 "Code action 'CorrectModels'"
var httpRequestService = ServiceProvider.GetService<HttpRequestService>();
        var httpRequest = httpRequestService.Request;
        UriBuilder uriBuilder = new UriBuilder(httpRequest.Uri);
        uriBuilder.Host = "devserv.natec.com";
        uriBuilder.Port = 9000;
        httpRequest.Uri = uriBuilder.Uri;
        return httpRequest;
#line default

    }
    
    private string CodeAction_FormResponse(CancellationToken CT, WorkflowItemTaskCodeAction Action, WorkflowTransition Transition, Models.HttpResponse Response)
    {
        //Common Service Funcs
        var ComeFrom = ActionServices.GetComeFromFunction(Transition);

#line 4 "Code action 'FormResponse'"
return Response.Content;
#line default

    }
    
    private Models.HttpResponse CodeAction_RestApi(CancellationToken CT, WorkflowItemTaskCodeAction Action, WorkflowTransition Transition, System.Uri Uri, string Method, string Login, string Password, Dictionary<string,string> Headers, string Body, string Encoding)
    {
             Logger.LogRestApi(Method, Uri, Headers, Body, Login, Password, Encoding);
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
                        request.Method = new HttpMethod(Method);
                        if (!string.IsNullOrEmpty(Body))
                        {
                            System.Text.Encoding encoding = !string.IsNullOrEmpty(Encoding) ?
                                System.Text.Encoding.GetEncoding(Encoding) :
                                System.Text.Encoding.UTF8;

                            /*
                            request.Content = !string.IsNullOrEmpty(content_type) ?
                                new StringContent(Body, encoding, content_type) :
                                new StringContent(Body, encoding);
                            */

                            request.Content = new StringContent(Body, encoding);
							if(!string.IsNullOrEmpty(content_type))
								request.Content.Headers.ContentType = System.Net.Http.Headers.MediaTypeHeaderValue.Parse(content_type);
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
 public static class WorkflowFactory_311_2
 {
     public static IWorkflowControl CreateWorkflow(IWorkflowController controller)
     {
         return new Natec.Workflow.Definition_311_2.WorkflowProcess(controller.InstanceId, controller.ServiceProvider, null);
     }
 }
}
