# SOAP Web Service Practical — Add Operation

## Complete Step-by-Step Guide

---

## **Aim**

To create, deploy, and test a simple SOAP-based web service in Java that performs an addition operation using NetBeans IDE and GlassFish Server.

---

## **Software Requirements**

- **NetBeans IDE** (version 8.2 or higher with Java EE support)
- **GlassFish Server** (version 4.1.1 or higher)
- **JDK** 8 or later
- **Web Browser** (Chrome, Firefox, or Edge for testing WSDL)
- **Optional:** SoapUI (for advanced SOAP testing)

---

## **Theory**

### What is SOAP?

**SOAP (Simple Object Access Protocol)** is a protocol for exchanging structured information in the implementation of web services. Key characteristics include:

- **XML-based messaging format:** All requests and responses are in XML
- **Protocol independence:** Can work over HTTP, SMTP, TCP, etc.
- **Platform and language independent:** Java, .NET, PHP, etc. can all consume SOAP services
- **Strongly typed:** Uses schemas to define data types

### What is WSDL?

**WSDL (Web Services Description Language)** is an XML-based language used to describe web services and how to access them. A WSDL file contains:

- **Service endpoint information** (URL where service is hosted)
- **Operations available** (methods that can be called)
- **Input/output parameters** (data types for requests and responses)
- **Binding details** (protocol and data format specifications)

### How SOAP Web Services Work

1. **Client** sends a SOAP request (XML) to the web service
2. **Server** processes the request
3. **Server** sends back a SOAP response (XML)
4. Communication happens over HTTP/HTTPS

---

## **Complete Procedure**

### **Step 1: Set Up Your Environment**

#### 1.1 Verify JDK Installation

Open Command Prompt/Terminal and run:

```bash
java -version
```

You should see Java version 1.8 or higher.

#### 1.2 Launch NetBeans IDE

- Start NetBeans IDE
- Ensure GlassFish Server is configured in Tools → Servers
- If not present, add it via Add Server → GlassFish Server → point to installation directory

---

### **Step 2: Create a New Web Application Project**

#### 2.1 Create New Project

1. Go to **File → New Project**
2. Select **Categories: Java Web** (or Java EE)
3. Select **Projects: Web Application**
4. Click **Next**

#### 2.2 Configure Project Settings

**Name and Location Screen:**
- **Project Name:** `SOAPPractical1` or `Soap_practical_1`
- **Project Location:** Leave default or choose your preferred location
- **Project Folder:** Auto-populated
- Click **Next**

#### 2.3 Server and Settings

**Server and Settings Screen:**
- **Server:** Select **GlassFish Server** (version 4.1.1 or your installed version)
- **Java EE Version:** Select **Java EE 6 Web** or **Java EE 7 Web**
- **Context Path:** Leave as default (`/SOAPPractical1`)
- Click **Next**

#### 2.4 Framework Selection

**Frameworks Screen:**
- Don't select any frameworks
- Click **Finish**

#### 2.5 Verify Project Structure

After creation, verify the project structure in the Projects panel:

```
SOAPPractical1
├── Web Pages
│   ├── WEB-INF
│   │   └── web.xml
│   └── index.html
├── Source Packages
│   └── (empty initially)
├── Test Packages
├── Libraries
└── Configuration Files
```

---

### **Step 3: Create the SOAP Web Service**

#### 3.1 Create Web Service

1. In **Projects** panel, **right-click** on **Source Packages**
2. Select **New → Web Service**
   - If you don't see "Web Service", select **New → Other**
   - Then choose **Categories: Web Services → File Types: Web Service**

#### 3.2 Configure Web Service

**New Web Service Dialog:**
- **Web Service Name:** `AddService`
- **Package:** `com.soap`
- Click **Finish**

NetBeans will generate a basic web service class file: `AddService.java`

#### 3.3 View Generated Code

The auto-generated code will look like this:

```java
package com.soap;

import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;

@WebService(serviceName = "AddService")
public class AddService {

    /**
     * This is a sample web service operation
     */
    @WebMethod(operationName = "hello")
    public String hello(@WebParam(name = "name") String txt) {
        return "Hello " + txt + " !";
    }
}
```

---

### **Step 4: Implement the Add Operation**

#### 4.1 Add the Addition Method

Replace or add the following method inside the `AddService` class:

```java
package com.soap;

import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;

@WebService(serviceName = "AddService")
public class AddService {

    /**
     * Web service operation to add two numbers
     */
    @WebMethod(operationName = "add")
    public int add(@WebParam(name = "num1") int num1, 
                   @WebParam(name = "num2") int num2) {
        return num1 + num2;
    }
    
    /**
     * This is a sample web service operation
     */
    @WebMethod(operationName = "hello")
    public String hello(@WebParam(name = "name") String txt) {
        return "Hello " + txt + " !";
    }
}
```

#### 4.2 Understanding the Code

**Annotations Explained:**

- `@WebService(serviceName = "AddService")`: Marks the class as a web service
- `@WebMethod(operationName = "add")`: Exposes the method as a web service operation
- `@WebParam(name = "num1")`: Names the parameter in the WSDL

**Method Details:**
- **Method name:** `add`
- **Parameters:** Two integers (`num1` and `num2`)
- **Return type:** Integer (sum of the two numbers)
- **Logic:** Simple addition operation

#### 4.3 Save the File

Press **Ctrl+S** (Windows/Linux) or **Cmd+S** (Mac) to save the file.

---

### **Step 5: Deploy the Web Service**

#### 5.1 Build the Project

1. **Right-click** on the project name (`SOAPPractical1`)
2. Select **Clean and Build**
3. Wait for the build to complete
4. Check the **Output** window for "BUILD SUCCESSFUL"

#### 5.2 Deploy to GlassFish Server

**Method 1: Direct Deployment**
1. **Right-click** on the project
2. Select **Deploy**
3. NetBeans will:
   - Start GlassFish Server (if not running)
   - Package the application as a WAR file
   - Deploy it to the server

**Method 2: Run the Project**
1. **Right-click** on the project
2. Select **Run**
3. This will build, deploy, and open a test page

#### 5.3 Verify Deployment

Check the **Output** window for deployment messages:

```
In-place deployment at C:\...\SOAPPractical1\build\web
GFv3 Server is running.
deploy?DEFAULT=C:\...\SOAPPractical1\build\web&name=SOAPPractical1&force=true finished in 1,234 ms
SOAPPractical1 was successfully deployed in 1,456 milliseconds.
```

---

### **Step 6: Test the Web Service**

#### 6.1 Access the WSDL

1. In **Projects** panel, expand **Web Services** node
2. **Right-click** on **AddService**
3. Select **Test Web Service**

This opens your browser with the WSDL URL:

```
http://localhost:8080/SOAPPractical1/AddService?WSDL
```

**Alternative:** Manually navigate to the URL in your browser.

#### 6.2 Understanding the WSDL Document

The WSDL file is XML and contains:

**Key Sections:**
- `<types>`: Data type definitions
- `<message>`: Input and output message formats
- `<portType>`: Available operations (add, hello)
- `<binding>`: Protocol details (SOAP over HTTP)
- `<service>`: Service endpoint URL

**Example WSDL snippet:**

```xml
<definitions targetNamespace="http://soap.com/" name="AddService">
  <types>...</types>
  <message name="add">
    <part name="num1" type="xsd:int"/>
    <part name="num2" type="xsd:int"/>
  </message>
  <message name="addResponse">
    <part name="return" type="xsd:int"/>
  </message>
  ...
</definitions>
```

#### 6.3 Test Using NetBeans Tester

When you select "Test Web Service", NetBeans opens a test page.

**Testing the `add` operation:**

1. NetBeans generates a test page automatically
2. You'll see available operations: `add` and `hello`
3. Click on **add**
4. Enter test values:
   - **num1:** `10`
   - **num2:** `20`
5. Click **Invoke** or **Call**

**Expected Result:**

You'll see the SOAP response:

```xml
<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
   <S:Body>
      <ns2:addResponse xmlns:ns2="http://soap.com/">
         <return>30</return>
      </ns2:addResponse>
   </S:Body>
</S:Envelope>
```

**Result:** `30` (sum of 10 + 20)

---

### **Step 7: Advanced Testing with SoapUI (Optional)**

#### 7.1 Install SoapUI

- Download SoapUI from https://www.soapui.org/
- Install and launch

#### 7.2 Create New SOAP Project

1. Click **File → New SOAP Project**
2. **Project Name:** `AddServiceTest`
3. **Initial WSDL:** `http://localhost:8080/SOAPPractical1/AddService?WSDL`
4. Click **OK**

#### 7.3 Test Operations

1. Expand the project tree: **AddService → AddServiceSoapBinding → add**
2. Double-click **Request 1**
3. Modify the XML request:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:soap="http://soap.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <soap:add>
         <num1>15</num1>
         <num2>25</num2>
      </soap:add>
   </soapenv:Body>
</soapenv:Envelope>
```

4. Click the green **Play** button
5. View the response in the right panel

**Expected Response:**

```xml
<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
   <S:Body>
      <ns2:addResponse xmlns:ns2="http://soap.com/">
         <return>40</return>
      </ns2:addResponse>
   </S:Body>
</S:Envelope>
```

---

## **Troubleshooting Guide**

### **Issue 1: GlassFish Server Not Starting**

**Error:** "GlassFish Server cannot start"

**Solutions:**
1. Check if port 8080 is already in use
   - Windows: `netstat -ano | findstr :8080`
   - Linux/Mac: `lsof -i :8080`
2. Kill the process or change GlassFish port
3. Restart NetBeans
4. Try starting server manually from Services tab

### **Issue 2: Web Service Not Found (404 Error)**

**Solutions:**
1. Verify deployment was successful in Output window
2. Check the correct URL format:
   ```
   http://localhost:8080/ProjectName/ServiceName?WSDL
   ```
3. Re-deploy the project (Right-click → Clean and Build → Deploy)
4. Restart GlassFish Server

### **Issue 3: WSDL Not Generated**

**Solutions:**
1. Ensure `@WebService` annotation is present on the class
2. Ensure `@WebMethod` annotation is on the methods
3. Clean and rebuild the project
4. Check for compilation errors in Output window

### **Issue 4: Cannot Find @WebService Annotation**

**Solutions:**
1. Ensure JDK (not JRE) is installed
2. Verify Java EE libraries are included in project
3. Add JAX-WS libraries manually if needed:
   - Right-click project → Properties → Libraries
   - Add JAX-WS 2.2 or higher

### **Issue 5: Port Already in Use**

**Error:** "Port 8080 is already in use"

**Solutions:**
1. **Change GlassFish port:**
   - Go to Services → Servers → GlassFish
   - Right-click → Properties
   - Change HTTP Port to 8081 or 9090
2. **Or kill the process using port 8080**

---

## **Understanding SOAP Messages**

### **SOAP Request Structure**

When you call the `add` operation, this XML request is sent:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:soap="http://soap.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <soap:add>
         <num1>10</num1>
         <num2>20</num2>
      </soap:add>
   </soapenv:Body>
</soapenv:Envelope>
```

**Components:**
- **Envelope:** Root element (mandatory)
- **Header:** Optional metadata
- **Body:** Contains the actual request (operation + parameters)

### **SOAP Response Structure**

The server returns:

```xml
<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
   <S:Body>
      <ns2:addResponse xmlns:ns2="http://soap.com/">
         <return>30</return>
      </ns2:addResponse>
   </S:Body>
</S:Envelope>
```

**Components:**
- **Envelope:** Root element
- **Body:** Contains the response
- **addResponse:** Operation response wrapper
- **return:** The result value

---

## **Additional Operations (Practice Exercises)**

Try adding these methods to enhance your web service:

### **1. Subtraction Operation**

```java
@WebMethod(operationName = "subtract")
public int subtract(@WebParam(name = "num1") int num1, 
                    @WebParam(name = "num2") int num2) {
    return num1 - num2;
}
```

### **2. Multiplication Operation**

```java
@WebMethod(operationName = "multiply")
public int multiply(@WebParam(name = "num1") int num1, 
                    @WebParam(name = "num2") int num2) {
    return num1 * num2;
}
```

### **3. Division Operation**

```java
@WebMethod(operationName = "divide")
public double divide(@WebParam(name = "num1") double num1, 
                     @WebParam(name = "num2") double num2) {
    if (num2 == 0) {
        throw new IllegalArgumentException("Cannot divide by zero");
    }
    return num1 / num2;
}
```

### **4. String Concatenation**

```java
@WebMethod(operationName = "concatenate")
public String concatenate(@WebParam(name = "str1") String str1, 
                          @WebParam(name = "str2") String str2) {
    return str1 + " " + str2;
}
```

After adding new methods:
1. **Save** the file
2. **Clean and Build** the project
3. **Re-deploy**
4. **Refresh** the WSDL in your browser to see new operations

---

## **Project File Structure**

After completion, your project structure should look like:

```
SOAPPractical1
├── Web Pages
│   ├── WEB-INF
│   │   ├── web.xml (auto-updated with service mappings)
│   │   └── sun-jaxws.xml (JAX-WS configuration)
│   └── index.html
├── Source Packages
│   └── com.soap
│       └── AddService.java (your web service)
├── Web Services
│   └── AddService (displayed node showing deployed service)
├── Libraries
│   ├── JDK 1.8
│   ├── GlassFish Server
│   └── JAX-WS libraries
└── Configuration Files
    └── Various XML configs
```

---

## **Key Takeaways**

✅ **SOAP** is an XML-based protocol for web services  
✅ **WSDL** describes the web service interface  
✅ **@WebService** annotation marks a class as a web service  
✅ **@WebMethod** exposes methods as service operations  
✅ **@WebParam** names parameters in WSDL  
✅ GlassFish automatically generates WSDL  
✅ Services are accessible via HTTP at `/ProjectName/ServiceName?WSDL`  

---

## **Conclusion**

You have successfully:
- Created a Java EE Web Application project
- Developed a SOAP-based web service with an addition operation
- Deployed the service to GlassFish Server
- Tested the service using WSDL and web-based tester
- Understood SOAP request/response structure

This practical demonstrates the fundamentals of SOAP web services, which are widely used in enterprise applications for system integration and interoperability.

---

## **References**

- [Oracle JAX-WS Documentation](https://docs.oracle.com/javaee/7/tutorial/jaxws.htm)
- [GlassFish Server Documentation](https://javaee.github.io/glassfish/)
- [SOAP Protocol Specification](https://www.w3.org/TR/soap/)
- [WSDL Specification](https://www.w3.org/TR/wsdl20/)

---

**End of Practical**
