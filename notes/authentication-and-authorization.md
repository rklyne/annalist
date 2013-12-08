
# Approval flow

This flow is activated when the client needs to establish the identity and approval of a user for obtaining subsequent authorization tokens.  The identity determination uses OpenID connect mechanisms, but does not result in grant of any specific permissions as these are handled separately by the authorization flow.

![Authentication flow sequence diagram](figures/authentication-flow.png "Authentication flow")

The approval request from browser to IDP includes a state value (nonce) provided by the client application, which is returned along with the approval code and should be checked when the approval code is returned.  This is a protection against cross-site request forgery (CSRF) attacks, in which another application tries to exploit a trust relationship between the browser and service.  The state value ensures that the browser request was indeed intiated by the client application.

@@TODO figure how the client state and params get encoded. (It looks as if it should be in the JSON that is POSTED to the auth service, but playground seems to not include the state param.  I may need some actual code to investigate.)  It seems that state is optional with OpenId Connect "Typically, Cross-Site Request Forgery (CSRF, XSRF) mitigation is done by cryptographically binding the value of this [state] parameter with the browser cookie.".

Sequence diagram definition - use with https://www.websequencediagrams.com/

    title Approval Flow
    
    Owner->Browser: (invokes)
    Browser->Client: (invokes)
    note right of Client:
      Client extablishes need
      for access permissions, and
      has not established a
      user id value
    end note
    
    Client->Browser: ("redirects" to IDP)
    Browser->IDP: (follows "redirection")
    note right of Client:
      This "redirection" may (mustbe?) be 
      by means of a form submission that
      includes the required parameters...?
    end note

    opt Browser is not logged in at IDP
        IDP->Browser: request owner credentials
        Browser->Owner: request cowner redentials
        Owner->Browser: owner credentials
        Browser->IDP: owner credentials
    end
    opt No existing record of approval of requested scope
        IDP->Browser: request approval
        Browser->Owner: request approval
        Owner->Browser: approval
        Browser->IDP: approval
    end
    IDP->Browser: (redirects to client+approval token)
    Browser->Client: (follows redirection+approval token)
    
    note right of Client:
      at this point, the client
      is in posession of an 
      authentication code and 
      a user id value
    end note

@@TODO: approval request to incude roles for which approval is required?  I.e. "scope" in OAuth2 flow.


# Authorization flow

This flow is activated when the client needs to obtain specific access 
permissions to a resource.  Unlike standard OAuth2 flows, this phase is 
separated from the authentication flow, so the access permissions may be
managed separately from the authentication and approval;  also, this 
phase does not depend on the owner being present at a browser to give
approval.

The client may the same or a different program to that which obtained 
the authentication token, in which case the authentication code may be 
passed by some unspecified means.

@@TODO: check that client id aspects still work here.

    title Authorization flow

    Owner->Browser: (invokes)
    Browser->Client: (invokes)
    note right of Client:
      Client has established
      identity of user, and
      needs grant of authority
      to access resource
    end note

    Client->Authorization svc: request permission (authentication code+client id+perms req)
    Authorization svc->Client: authorization code

    note right of Client:
      at this point, the client
      is in posession of an 
      authorization code and
      possibly a refresh code

@@TODO: revisit UMA and see if UMA elements can be repurposed to fit the requirements.


# Resource access flow

This flow should be the same as the corresponding phase of the OAuth2 flows.

@@TODO: flesh this out to include details of refresh, where needed.

    title Resource access flow

    Owner->Browser: (invokes)
    Browser->Client: (invokes)
    note right of Client:
      Client needs to access resource,
      and is in possession of an
      authorization code.
    end note

    Client->Authorization svc: request access (authorization code)
    Authorization svc->Client: access token

    note right of Client:
      at this point, the client
      is in posession of an 
      access token
    end note

    Client->Resource svc: request + access token
    Resource svc->Client: (data or response)

