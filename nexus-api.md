1. Get method info.
Gets the execution info of the method or the methods in a class..

Request.
curl -X 'GET' \
  'http://localhost:8081/test/api/method-graph-paths/mpks?serviceName=codetrails&className=com.example.codetrails.orders.util.OrderUtil&profilingInfo=true&step=1m' \
  -H 'accept: */*'

There is an optional parameter called methodName.. That can be given to get the method details for a class and method name.

Response
[
  {
    "id": null,
    "domainName": "test",
    "serviceName": "codetrails",
    "methodDetailsHash": -909416830,
    "className": "com.example.codetrails.orders.util.OrderUtil",
    "methodName": "enrichOrder(Lcom/example/codetrails/orders/model/Order;)Ljava/lang/String;",
    "methodNameOnly": "enrichOrder",
    "methodParams": [
      "com.example.codetrails.orders.model.Order"
    ],
    "qps": 19.77,
    "qpm": 1186.53,
    "counterValue": 4785.9400000000005,
    "errorRate": 0,
    "latencyms": 0,
    "errorRatePct": 0,
    "httpRoute": null,
    "httpMethod": null,
    "cpuUtilizationPercent": 0,
    "controllerMethod": false
  },
  {
    "id": null,
    "domainName": "test",
    "serviceName": "codetrails",
    "methodDetailsHash": -702075508,
    "className": "com.example.codetrails.orders.util.OrderUtil",
    "methodName": "validateUserContext(Ljava/lang/String;)Z",
    "methodNameOnly": "validateUserContext",
    "methodParams": [
      "java.lang.String"
    ],
    "qps": 1.7,
    "qpm": 102.11,
    "counterValue": 405.55,
    "errorRate": 0,
    "latencyms": 0,
    "errorRatePct": 0,
    "httpRoute": null,
    "httpMethod": null,
    "cpuUtilizationPercent": 0,
    "controllerMethod": false
  }
]




2. Get Flows
Gets the list of flowIds that a method is a part of.

Request
curl -X 'GET' \
  'http://localhost:8081/test/api/method-graph-paths/flows?serviceName=codetrails&className=com.example.codetrails.orders.util.OrderUtil&step=1m' \
  -H 'accept: */*'

There is an optional parameter called methodName.. That can be given to get the method details for a class and method name.


Response
[
  {
    "methodSignature": {
      "id": 10054,
      "domainName": "test",
      "serviceName": "codetrails",
      "methodDetailsHash": -702075508,
      "className": "com.example.codetrails.orders.util.OrderUtil",
      "methodName": "validateUserContext(Ljava/lang/String;)Z",
      "methodNameOnly": "validateUserContext",
      "methodParams": [
        "java.lang.String"
      ],
      "additionalInfo": null
    },
    "flowIds": [
      1229045550,
      1761630448,
      1100248077
    ]
  },
  {
    "methodSignature": {
      "id": 9994,
      "domainName": "test",
      "serviceName": "codetrails",
      "methodDetailsHash": -909416830,
      "className": "com.example.codetrails.orders.util.OrderUtil",
      "methodName": "enrichOrder(Lcom/example/codetrails/orders/model/Order;)Ljava/lang/String;",
      "methodNameOnly": "enrichOrder",
      "methodParams": [
        "com.example.codetrails.orders.model.Order"
      ],
      "additionalInfo": null
    },
    "flowIds": [
      -647673835,
      168381800,
      1229045550,
      -174297302,
      1100248077,
      -1195429020
    ]
  }
]


3. Flow Details
Takes a list of flowIds and returns the entire path (including branches) the flow has taken. The response has a tree line format.

Request
curl -X 'GET' \
  'http://localhost:8081/test/api/method-graph-paths/flow-details?serviceName=codetrails&flowIds=168381800&flowIds=1229045550&step=1m' \
  -H 'accept: */*'

You can give multiple flowIds as shown above.

Response
{
  "168381800": {
    "element": {
      "id": null,
      "domainName": "test",
      "serviceName": "codetrails",
      "methodDetailsHash": 1559491099,
      "className": "com.example.codetrails.config.RequestLogFilter",
      "methodName": "doFilterInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljavax/servlet/FilterChain;)V",
      "methodNameOnly": "doFilterInternal",
      "methodParams": [
        "javax.servlet.http.HttpServletRequest",
        "javax.servlet.http.HttpServletResponse",
        "javax.servlet.FilterChain"
      ],
      "qps": 0.1,
      "qpm": 6.08,
      "counterValue": 27.23,
      "errorRate": 0,
      "latencyms": 0,
      "errorRatePct": 0,
      "httpRoute": null,
      "httpMethod": null,
      "cpuUtilizationPercent": 0,
      "controllerMethod": false
    },
    "parentMpk": 0,
    "children": {
      "-1280925096": {
        "element": {
          "id": null,
          "domainName": "test",
          "serviceName": "codetrails",
          "methodDetailsHash": 1914427635,
          "className": "com.example.codetrails.config.CustomAccessLogFilter",
          "methodName": "doFilterInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljavax/servlet/FilterChain;)V",
          "methodNameOnly": "doFilterInternal",
          "methodParams": [
            "javax.servlet.http.HttpServletRequest",
            "javax.servlet.http.HttpServletResponse",
            "javax.servlet.FilterChain"
          ],
          "qps": 0.1,
          "qpm": 6.08,
          "counterValue": 27.23,
          "errorRate": 0,
          "latencyms": 0,
          "errorRatePct": 0,
          "httpRoute": null,
          "httpMethod": null,
          "cpuUtilizationPercent": 0,
          "controllerMethod": false
        },
        "parentMpk": 1559492060,
        "children": {
          "256455610": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": 1310426961,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getStatus()Ljava/lang/String;",
              "methodNameOnly": "getStatus",
              "methodParams": [],
              "qps": 0.1,
              "qpm": 6.08,
              "counterValue": 27.23,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": 256455610
          },
          "496547308": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": 1550518659,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getMetadata()Ljava/util/Map;",
              "methodNameOnly": "getMetadata",
              "methodParams": [],
              "qps": 0.1,
              "qpm": 6.08,
              "counterValue": 27.23,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": 496547308
          },
          "1499787480": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -1741208465,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getId()Ljava/lang/Long;",
              "methodNameOnly": "getId",
              "methodParams": [],
              "qps": 0.1,
              "qpm": 6.08,
              "counterValue": 27.23,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": 1499787480
          },
          "1965198262": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -1275797683,
              "className": "com.example.codetrails.config.CustomAccessLogFilter",
              "methodName": "isExcludedPath(Ljava/lang/String;)Z",
              "methodNameOnly": "isExcludedPath",
              "methodParams": [
                "java.lang.String"
              ],
              "qps": 0.1,
              "qpm": 6.08,
              "counterValue": 27.23,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": 1965198262
          },
          "-2010715945": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -956744594,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getCreatedAt()Ljava/time/LocalDateTime;",
              "methodNameOnly": "getCreatedAt",
              "methodParams": [],
              "qps": 0.1,
              "qpm": 6.08,
              "counterValue": 27.23,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": -2010715945
          },
          "-71302014": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": 982669337,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getType()Ljava/lang/String;",
              "methodNameOnly": "getType",
              "methodParams": [],
              "qps": 0.1,
              "qpm": 6.08,
              "counterValue": 27.23,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": -71302014
          },
          "-1610030752": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -556059401,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getAmount()Ljava/lang/Double;",
              "methodNameOnly": "getAmount",
              "methodParams": [],
              "qps": 0.1,
              "qpm": 6.08,
              "counterValue": 27.23,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": -1610030752
          },
          "-1766119199": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -712147848,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getCustomerId()Ljava/lang/String;",
              "methodNameOnly": "getCustomerId",
              "methodParams": [],
              "qps": 0.1,
              "qpm": 6.08,
              "counterValue": 27.23,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": -1766119199
          },
          "-100871214": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -598673540,
              "className": "com.example.codetrails.orders.controller.OrderController",
              "methodName": "getOrderById(Ljava/lang/Long;)Lorg/springframework/http/ResponseEntity;",
              "methodNameOnly": "getOrderById",
              "methodParams": [
                "java.lang.Long"
              ],
              "qps": 0.1,
              "qpm": 6.08,
              "counterValue": 27.23,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": "/api/orders/{orderId}",
              "httpMethod": "GET",
              "cpuUtilizationPercent": 0,
              "controllerMethod": true
            },
            "parentMpk": -1280925096,
            "children": {
              "652522101": {
                "element": {
                  "id": null,
                  "domainName": "test",
                  "serviceName": "codetrails",
                  "methodDetailsHash": -515438522,
                  "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                  "methodName": "getOrderById(Ljava/lang/Long;)Lcom/example/codetrails/orders/model/Order;",
                  "methodNameOnly": "getOrderById",
                  "methodParams": [
                    "java.lang.Long"
                  ],
                  "qps": 0.1,
                  "qpm": 6.08,
                  "counterValue": 27.23,
                  "errorRate": 0,
                  "latencyms": 0,
                  "errorRatePct": 0,
                  "httpRoute": null,
                  "httpMethod": null,
                  "cpuUtilizationPercent": 0,
                  "controllerMethod": false
                },
                "parentMpk": -100871214,
                "children": {
                  "446251425": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": 1692901813,
                      "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                      "methodName": "fallbackOrderHandler(Lcom/example/codetrails/orders/model/Order;)V",
                      "methodNameOnly": "fallbackOrderHandler",
                      "methodParams": [
                        "com.example.codetrails.orders.model.Order"
                      ],
                      "qps": 0.1,
                      "qpm": 6.08,
                      "counterValue": 27.23,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 652522101,
                    "children": {
                      "325979020": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -622914228,
                          "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                          "methodName": "logIssue(Lcom/example/codetrails/orders/model/Order;)V",
                          "methodNameOnly": "logIssue",
                          "methodParams": [
                            "com.example.codetrails.orders.model.Order"
                          ],
                          "qps": 0.1,
                          "qpm": 6.08,
                          "counterValue": 27.23,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": 446251425,
                        "children": {
                          "-225792476": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": -1741208465,
                              "className": "com.example.codetrails.orders.model.Order",
                              "methodName": "getId()Ljava/lang/Long;",
                              "methodNameOnly": "getId",
                              "methodParams": [],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": 325979020,
                            "children": {},
                            "mpk": -225792476
                          }
                        },
                        "mpk": 325979020
                      },
                      "661137513": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -287755735,
                          "className": "com.example.codetrails.orders.model.Order",
                          "methodName": "setStatus(Ljava/lang/String;)V",
                          "methodNameOnly": "setStatus",
                          "methodParams": [
                            "java.lang.String"
                          ],
                          "qps": 0.1,
                          "qpm": 6.08,
                          "counterValue": 27.23,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": 446251425,
                        "children": {},
                        "mpk": 661137513
                      },
                      "-1914367903": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": 1431706145,
                          "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                          "methodName": "triggerManualOverride(Lcom/example/codetrails/orders/model/Order;)V",
                          "methodNameOnly": "triggerManualOverride",
                          "methodParams": [
                            "com.example.codetrails.orders.model.Order"
                          ],
                          "qps": 0.1,
                          "qpm": 6.08,
                          "counterValue": 27.23,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": 446251425,
                        "children": {
                          "-957070353": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": -1741208465,
                              "className": "com.example.codetrails.orders.model.Order",
                              "methodName": "getId()Ljava/lang/Long;",
                              "methodNameOnly": "getId",
                              "methodParams": [],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -1914367903,
                            "children": {},
                            "mpk": -957070353
                          }
                        },
                        "mpk": -1914367903
                      },
                      "-792315217": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -1741208465,
                          "className": "com.example.codetrails.orders.model.Order",
                          "methodName": "getId()Ljava/lang/Long;",
                          "methodNameOnly": "getId",
                          "methodParams": [],
                          "qps": 0.1,
                          "qpm": 6.08,
                          "counterValue": 27.23,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": 446251425,
                        "children": {},
                        "mpk": -792315217
                      },
                      "-468742063": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -1417635311,
                          "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                          "methodName": "notifyWarehouse(Lcom/example/codetrails/orders/model/Order;)V",
                          "methodNameOnly": "notifyWarehouse",
                          "methodParams": [
                            "com.example.codetrails.orders.model.Order"
                          ],
                          "qps": 0.1,
                          "qpm": 6.08,
                          "counterValue": 27.23,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": 446251425,
                        "children": {
                          "907657727": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": -1741208465,
                              "className": "com.example.codetrails.orders.model.Order",
                              "methodName": "getId()Ljava/lang/Long;",
                              "methodNameOnly": "getId",
                              "methodParams": [],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -468742063,
                            "children": {},
                            "mpk": 907657727
                          }
                        },
                        "mpk": -468742063
                      }
                    },
                    "mpk": 446251425
                  },
                  "1307108443": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": -1741208465,
                      "className": "com.example.codetrails.orders.model.Order",
                      "methodName": "getId()Ljava/lang/Long;",
                      "methodNameOnly": "getId",
                      "methodParams": [],
                      "qps": 1.6400000000000001,
                      "qpm": 98.31,
                      "counterValue": 472.87,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 652522101,
                    "children": {},
                    "mpk": 1307108443
                  },
                  "2138900078": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": -909416830,
                      "className": "com.example.codetrails.orders.util.OrderUtil",
                      "methodName": "enrichOrder(Lcom/example/codetrails/orders/model/Order;)Ljava/lang/String;",
                      "methodNameOnly": "enrichOrder",
                      "methodParams": [
                        "com.example.codetrails.orders.model.Order"
                      ],
                      "qps": 0.1,
                      "qpm": 6.08,
                      "counterValue": 27.23,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 652522101,
                    "children": {},
                    "mpk": 2138900078
                  },
                  "-263981051": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": 982669337,
                      "className": "com.example.codetrails.orders.model.Order",
                      "methodName": "getType()Ljava/lang/String;",
                      "methodNameOnly": "getType",
                      "methodParams": [],
                      "qps": 0.1,
                      "qpm": 6.08,
                      "counterValue": 27.23,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 652522101,
                    "children": {},
                    "mpk": -263981051
                  },
                  "-175254476": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": 1071395912,
                      "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                      "methodName": "createMockOrder(Ljava/lang/Long;)Lcom/example/codetrails/orders/model/Order;",
                      "methodNameOnly": "createMockOrder",
                      "methodParams": [
                        "java.lang.Long"
                      ],
                      "qps": 0.1,
                      "qpm": 6.08,
                      "counterValue": 27.23,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 652522101,
                    "children": {},
                    "mpk": -175254476
                  },
                  "-1785295221": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": -538644833,
                      "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                      "methodName": "processPhysicalOrder(Lcom/example/codetrails/orders/model/Order;)V",
                      "methodNameOnly": "processPhysicalOrder",
                      "methodParams": [
                        "com.example.codetrails.orders.model.Order"
                      ],
                      "qps": 0.1,
                      "qpm": 6.08,
                      "counterValue": 27.23,
                      "errorRate": 0.1,
                      "latencyms": 0,
                      "errorRatePct": 100,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 652522101,
                    "children": {
                      "-578927574": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -1069351532,
                          "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                          "methodName": "dispatchToVendor(Lcom/example/codetrails/orders/model/Order;)V",
                          "methodNameOnly": "dispatchToVendor",
                          "methodParams": [
                            "com.example.codetrails.orders.model.Order"
                          ],
                          "qps": 0.1,
                          "qpm": 6.08,
                          "counterValue": 27.23,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": -1785295221,
                        "children": {
                          "1786874182": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": -1741208465,
                              "className": "com.example.codetrails.orders.model.Order",
                              "methodName": "getId()Ljava/lang/Long;",
                              "methodNameOnly": "getId",
                              "methodParams": [],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -578927574,
                            "children": {},
                            "mpk": 1786874182
                          }
                        },
                        "mpk": -578927574
                      },
                      "-1250784507": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -1741208465,
                          "className": "com.example.codetrails.orders.model.Order",
                          "methodName": "getId()Ljava/lang/Long;",
                          "methodNameOnly": "getId",
                          "methodParams": [],
                          "qps": 0.30000000000000004,
                          "qpm": 18.23,
                          "counterValue": 81.68,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": -1785295221,
                        "children": {},
                        "mpk": -1250784507
                      },
                      "-1402284269": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -1892708227,
                          "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                          "methodName": "validateInventory(Lcom/example/codetrails/orders/model/Order;)V",
                          "methodNameOnly": "validateInventory",
                          "methodParams": [
                            "com.example.codetrails.orders.model.Order"
                          ],
                          "qps": 0.1,
                          "qpm": 6.08,
                          "counterValue": 27.23,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": -1785295221,
                        "children": {
                          "759035041": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": 1280173459,
                              "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                              "methodName": "fetchStock(Lcom/example/codetrails/orders/model/Order;)V",
                              "methodNameOnly": "fetchStock",
                              "methodParams": [
                                "com.example.codetrails.orders.model.Order"
                              ],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -1402284269,
                            "children": {
                              "314042287": {
                                "element": {
                                  "id": null,
                                  "domainName": "test",
                                  "serviceName": "codetrails",
                                  "methodDetailsHash": -1741208465,
                                  "className": "com.example.codetrails.orders.model.Order",
                                  "methodName": "getId()Ljava/lang/Long;",
                                  "methodNameOnly": "getId",
                                  "methodParams": [],
                                  "qps": 0.1,
                                  "qpm": 6.08,
                                  "counterValue": 27.23,
                                  "errorRate": 0,
                                  "latencyms": 0,
                                  "errorRatePct": 0,
                                  "httpRoute": null,
                                  "httpMethod": null,
                                  "cpuUtilizationPercent": 0,
                                  "controllerMethod": false
                                },
                                "parentMpk": 759035041,
                                "children": {},
                                "mpk": 314042287
                              }
                            },
                            "mpk": 759035041
                          },
                          "2032620413": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": -1741208465,
                              "className": "com.example.codetrails.orders.model.Order",
                              "methodName": "getId()Ljava/lang/Long;",
                              "methodNameOnly": "getId",
                              "methodParams": [],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -1402284269,
                            "children": {},
                            "mpk": 2032620413
                          },
                          "-1479962496": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": -958824078,
                              "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                              "methodName": "checkWarehouse(Lcom/example/codetrails/orders/model/Order;)V",
                              "methodNameOnly": "checkWarehouse",
                              "methodParams": [
                                "com.example.codetrails.orders.model.Order"
                              ],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -1402284269,
                            "children": {
                              "-375404624": {
                                "element": {
                                  "id": null,
                                  "domainName": "test",
                                  "serviceName": "codetrails",
                                  "methodDetailsHash": -1741208465,
                                  "className": "com.example.codetrails.orders.model.Order",
                                  "methodName": "getId()Ljava/lang/Long;",
                                  "methodNameOnly": "getId",
                                  "methodParams": [],
                                  "qps": 0.1,
                                  "qpm": 6.08,
                                  "counterValue": 27.23,
                                  "errorRate": 0,
                                  "latencyms": 0,
                                  "errorRatePct": 0,
                                  "httpRoute": null,
                                  "httpMethod": null,
                                  "cpuUtilizationPercent": 0,
                                  "controllerMethod": false
                                },
                                "parentMpk": -1479962496,
                                "children": {},
                                "mpk": -375404624
                              }
                            },
                            "mpk": -1479962496
                          },
                          "-561857911": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": -40719493,
                              "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                              "methodName": "reserveItems(Lcom/example/codetrails/orders/model/Order;)V",
                              "methodNameOnly": "reserveItems",
                              "methodParams": [
                                "com.example.codetrails.orders.model.Order"
                              ],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -1402284269,
                            "children": {
                              "-1978933561": {
                                "element": {
                                  "id": null,
                                  "domainName": "test",
                                  "serviceName": "codetrails",
                                  "methodDetailsHash": -1741208465,
                                  "className": "com.example.codetrails.orders.model.Order",
                                  "methodName": "getId()Ljava/lang/Long;",
                                  "methodNameOnly": "getId",
                                  "methodParams": [],
                                  "qps": 0.1,
                                  "qpm": 6.08,
                                  "counterValue": 27.23,
                                  "errorRate": 0,
                                  "latencyms": 0,
                                  "errorRatePct": 0,
                                  "httpRoute": null,
                                  "httpMethod": null,
                                  "cpuUtilizationPercent": 0,
                                  "controllerMethod": false
                                },
                                "parentMpk": -561857911,
                                "children": {},
                                "mpk": -1978933561
                              }
                            },
                            "mpk": -561857911
                          }
                        },
                        "mpk": -1402284269
                      },
                      "-1485864669": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -1976288627,
                          "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                          "methodName": "estimateShipping(Lcom/example/codetrails/orders/model/Order;)V",
                          "methodNameOnly": "estimateShipping",
                          "methodParams": [
                            "com.example.codetrails.orders.model.Order"
                          ],
                          "qps": 0.1,
                          "qpm": 6.08,
                          "counterValue": 27.23,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": -1785295221,
                        "children": {
                          "1170732996": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": -12103482,
                              "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                              "methodName": "calculateDeliveryRoute(Lcom/example/codetrails/orders/model/Order;)V",
                              "methodNameOnly": "calculateDeliveryRoute",
                              "methodParams": [
                                "com.example.codetrails.orders.model.Order"
                              ],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -1485864669,
                            "children": {
                              "191777004": {
                                "element": {
                                  "id": null,
                                  "domainName": "test",
                                  "serviceName": "codetrails",
                                  "methodDetailsHash": -1741208465,
                                  "className": "com.example.codetrails.orders.model.Order",
                                  "methodName": "getId()Ljava/lang/Long;",
                                  "methodNameOnly": "getId",
                                  "methodParams": [],
                                  "qps": 0.1,
                                  "qpm": 6.08,
                                  "counterValue": 27.23,
                                  "errorRate": 0,
                                  "latencyms": 0,
                                  "errorRatePct": 0,
                                  "httpRoute": null,
                                  "httpMethod": null,
                                  "cpuUtilizationPercent": 0,
                                  "controllerMethod": false
                                },
                                "parentMpk": 1170732996,
                                "children": {},
                                "mpk": 191777004
                              }
                            },
                            "mpk": 1170732996
                          },
                          "-1112530153": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": 1999600665,
                              "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                              "methodName": "getShippingCosts(Lcom/example/codetrails/orders/model/Order;)V",
                              "methodNameOnly": "getShippingCosts",
                              "methodParams": [
                                "com.example.codetrails.orders.model.Order"
                              ],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -1485864669,
                            "children": {
                              "-1869903879": {
                                "element": {
                                  "id": null,
                                  "domainName": "test",
                                  "serviceName": "codetrails",
                                  "methodDetailsHash": -1741208465,
                                  "className": "com.example.codetrails.orders.model.Order",
                                  "methodName": "getId()Ljava/lang/Long;",
                                  "methodNameOnly": "getId",
                                  "methodParams": [],
                                  "qps": 0.1,
                                  "qpm": 6.08,
                                  "counterValue": 27.23,
                                  "errorRate": 0,
                                  "latencyms": 0,
                                  "errorRatePct": 0,
                                  "httpRoute": null,
                                  "httpMethod": null,
                                  "cpuUtilizationPercent": 0,
                                  "controllerMethod": false
                                },
                                "parentMpk": -1112530153,
                                "children": {},
                                "mpk": -1869903879
                              }
                            },
                            "mpk": -1112530153
                          },
                          "-558371987": {
                            "element": {
                              "id": null,
                              "domainName": "test",
                              "serviceName": "codetrails",
                              "methodDetailsHash": -1741208465,
                              "className": "com.example.codetrails.orders.model.Order",
                              "methodName": "getId()Ljava/lang/Long;",
                              "methodNameOnly": "getId",
                              "methodParams": [],
                              "qps": 0.1,
                              "qpm": 6.08,
                              "counterValue": 27.23,
                              "errorRate": 0,
                              "latencyms": 0,
                              "errorRatePct": 0,
                              "httpRoute": null,
                              "httpMethod": null,
                              "cpuUtilizationPercent": 0,
                              "controllerMethod": false
                            },
                            "parentMpk": -1485864669,
                            "children": {},
                            "mpk": -558371987
                          }
                        },
                        "mpk": -1485864669
                      }
                    },
                    "mpk": -1785295221
                  }
                },
                "mpk": 652522101
              }
            },
            "mpk": -100871214
          }
        },
        "mpk": -1280925096
      }
    },
    "mpk": 1559492060
  },
  "1229045550": {
    "element": {
      "id": null,
      "domainName": "test",
      "serviceName": "codetrails",
      "methodDetailsHash": 1559491099,
      "className": "com.example.codetrails.config.RequestLogFilter",
      "methodName": "doFilterInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljavax/servlet/FilterChain;)V",
      "methodNameOnly": "doFilterInternal",
      "methodParams": [
        "javax.servlet.http.HttpServletRequest",
        "javax.servlet.http.HttpServletResponse",
        "javax.servlet.FilterChain"
      ],
      "qps": 1.27,
      "qpm": 76.28,
      "counterValue": 240.73,
      "errorRate": 0,
      "latencyms": 0,
      "errorRatePct": 0,
      "httpRoute": null,
      "httpMethod": null,
      "cpuUtilizationPercent": 0,
      "controllerMethod": false
    },
    "parentMpk": 0,
    "children": {
      "-1280925096": {
        "element": {
          "id": null,
          "domainName": "test",
          "serviceName": "codetrails",
          "methodDetailsHash": 1914427635,
          "className": "com.example.codetrails.config.CustomAccessLogFilter",
          "methodName": "doFilterInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljavax/servlet/FilterChain;)V",
          "methodNameOnly": "doFilterInternal",
          "methodParams": [
            "javax.servlet.http.HttpServletRequest",
            "javax.servlet.http.HttpServletResponse",
            "javax.servlet.FilterChain"
          ],
          "qps": 1.27,
          "qpm": 76.28,
          "counterValue": 240.73,
          "errorRate": 0,
          "latencyms": 0,
          "errorRatePct": 0,
          "httpRoute": null,
          "httpMethod": null,
          "cpuUtilizationPercent": 0,
          "controllerMethod": false
        },
        "parentMpk": 1559492060,
        "children": {
          "256455610": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": 1310426961,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getStatus()Ljava/lang/String;",
              "methodNameOnly": "getStatus",
              "methodParams": [],
              "qps": 24.22,
              "qpm": 1453.2,
              "counterValue": 4666.87,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": 256455610
          },
          "496547308": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": 1550518659,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getMetadata()Ljava/util/Map;",
              "methodNameOnly": "getMetadata",
              "methodParams": [],
              "qps": 24.22,
              "qpm": 1453.2,
              "counterValue": 4666.87,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": 496547308
          },
          "1499787480": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -1741208465,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getId()Ljava/lang/Long;",
              "methodNameOnly": "getId",
              "methodParams": [],
              "qps": 24.22,
              "qpm": 1453.2,
              "counterValue": 4666.87,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": 1499787480
          },
          "1965198262": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -1275797683,
              "className": "com.example.codetrails.config.CustomAccessLogFilter",
              "methodName": "isExcludedPath(Ljava/lang/String;)Z",
              "methodNameOnly": "isExcludedPath",
              "methodParams": [
                "java.lang.String"
              ],
              "qps": 1.27,
              "qpm": 76.28,
              "counterValue": 240.73,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": 1965198262
          },
          "-2010715945": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -956744594,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getCreatedAt()Ljava/time/LocalDateTime;",
              "methodNameOnly": "getCreatedAt",
              "methodParams": [],
              "qps": 24.22,
              "qpm": 1453.2,
              "counterValue": 4666.87,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": -2010715945
          },
          "-71302014": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": 982669337,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getType()Ljava/lang/String;",
              "methodNameOnly": "getType",
              "methodParams": [],
              "qps": 24.22,
              "qpm": 1453.2,
              "counterValue": 4666.87,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": -71302014
          },
          "-1048257232": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": 1312594138,
              "className": "com.example.codetrails.orders.controller.OrderController",
              "methodName": "getAllOrders(Ljava/lang/String;Ljava/lang/Integer;)Lorg/springframework/http/ResponseEntity;",
              "methodNameOnly": "getAllOrders",
              "methodParams": [
                "java.lang.String",
                "java.lang.Integer"
              ],
              "qps": 1.27,
              "qpm": 76.28,
              "counterValue": 240.73,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": "/api/orders",
              "httpMethod": "GET",
              "cpuUtilizationPercent": 0,
              "controllerMethod": true
            },
            "parentMpk": -1280925096,
            "children": {
              "1251787835": {
                "element": {
                  "id": null,
                  "domainName": "test",
                  "serviceName": "codetrails",
                  "methodDetailsHash": -611977302,
                  "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                  "methodName": "getAllOrders(Ljava/lang/String;Ljava/lang/Integer;)Ljava/util/List;",
                  "methodNameOnly": "getAllOrders",
                  "methodParams": [
                    "java.lang.String",
                    "java.lang.Integer"
                  ],
                  "qps": 1.27,
                  "qpm": 76.28,
                  "counterValue": 240.73,
                  "errorRate": 0,
                  "latencyms": 0,
                  "errorRatePct": 0,
                  "httpRoute": null,
                  "httpMethod": null,
                  "cpuUtilizationPercent": 0,
                  "controllerMethod": false
                },
                "parentMpk": -1048257232,
                "children": {
                  "1665549425": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": 1514831243,
                      "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                      "methodName": "sortByRecentActivity(Ljava/util/List;)Ljava/util/List;",
                      "methodNameOnly": "sortByRecentActivity",
                      "methodParams": [
                        "java.util.List"
                      ],
                      "qps": 1.27,
                      "qpm": 76.28,
                      "counterValue": 240.73,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 1251787835,
                    "children": {
                      "-864319010": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -956744594,
                          "className": "com.example.codetrails.orders.model.Order",
                          "methodName": "getCreatedAt()Ljava/time/LocalDateTime;",
                          "methodNameOnly": "getCreatedAt",
                          "methodParams": [],
                          "qps": 46.120000000000005,
                          "qpm": 2767.52,
                          "counterValue": 8853.71,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": 1665549425,
                        "children": {},
                        "mpk": -864319010
                      }
                    },
                    "mpk": 1665549425
                  },
                  "1959219694": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": 1808501512,
                      "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                      "methodName": "filterOrdersByStatus(Ljava/util/List;Ljava/lang/String;)Ljava/util/List;",
                      "methodNameOnly": "filterOrdersByStatus",
                      "methodParams": [
                        "java.util.List",
                        "java.lang.String"
                      ],
                      "qps": 1.27,
                      "qpm": 76.28,
                      "counterValue": 240.73,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 1251787835,
                    "children": {
                      "1916696292": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": 1310426961,
                          "className": "com.example.codetrails.orders.model.Order",
                          "methodName": "getStatus()Ljava/lang/String;",
                          "methodNameOnly": "getStatus",
                          "methodParams": [],
                          "qps": 25.43,
                          "qpm": 1525.66,
                          "counterValue": 4814.669999999999,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": 1959219694,
                        "children": {},
                        "mpk": 1916696292
                      }
                    },
                    "mpk": 1959219694
                  },
                  "-551357326": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": -702075508,
                      "className": "com.example.codetrails.orders.util.OrderUtil",
                      "methodName": "validateUserContext(Ljava/lang/String;)Z",
                      "methodNameOnly": "validateUserContext",
                      "methodParams": [
                        "java.lang.String"
                      ],
                      "qps": 1.27,
                      "qpm": 76.28,
                      "counterValue": 240.73,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 1251787835,
                    "children": {},
                    "mpk": -551357326
                  },
                  "-692499673": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": -843217855,
                      "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                      "methodName": "calculateTotals(Ljava/util/List;)Ljava/util/List;",
                      "methodNameOnly": "calculateTotals",
                      "methodParams": [
                        "java.util.List"
                      ],
                      "qps": 1.27,
                      "qpm": 76.28,
                      "counterValue": 240.73,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 1251787835,
                    "children": {
                      "-548711823": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -556059401,
                          "className": "com.example.codetrails.orders.model.Order",
                          "methodName": "getAmount()Ljava/lang/Double;",
                          "methodNameOnly": "getAmount",
                          "methodParams": [],
                          "qps": 24.33,
                          "qpm": 1460.04,
                          "counterValue": 4666.87,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": -692499673,
                        "children": {},
                        "mpk": -548711823
                      }
                    },
                    "mpk": -692499673
                  },
                  "-758698648": {
                    "element": {
                      "id": null,
                      "domainName": "test",
                      "serviceName": "codetrails",
                      "methodDetailsHash": -909416830,
                      "className": "com.example.codetrails.orders.util.OrderUtil",
                      "methodName": "enrichOrder(Lcom/example/codetrails/orders/model/Order;)Ljava/lang/String;",
                      "methodNameOnly": "enrichOrder",
                      "methodParams": [
                        "com.example.codetrails.orders.model.Order"
                      ],
                      "qps": 24.22,
                      "qpm": 1453.2,
                      "counterValue": 4666.87,
                      "errorRate": 0,
                      "latencyms": 0,
                      "errorRatePct": 0,
                      "httpRoute": null,
                      "httpMethod": null,
                      "cpuUtilizationPercent": 0,
                      "controllerMethod": false
                    },
                    "parentMpk": 1251787835,
                    "children": {
                      "508938184": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -1741208465,
                          "className": "com.example.codetrails.orders.model.Order",
                          "methodName": "getId()Ljava/lang/Long;",
                          "methodNameOnly": "getId",
                          "methodParams": [],
                          "qps": 24.22,
                          "qpm": 1453.2,
                          "counterValue": 4666.87,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": -758698648,
                        "children": {},
                        "mpk": 508938184
                      },
                      "1537998801": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": -712147848,
                          "className": "com.example.codetrails.orders.model.Order",
                          "methodName": "getCustomerId()Ljava/lang/String;",
                          "methodNameOnly": "getCustomerId",
                          "methodParams": [],
                          "qps": 24.22,
                          "qpm": 1453.2,
                          "counterValue": 4666.87,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": -758698648,
                        "children": {},
                        "mpk": 1537998801
                      },
                      "-494301988": {
                        "element": {
                          "id": null,
                          "domainName": "test",
                          "serviceName": "codetrails",
                          "methodDetailsHash": 1550518659,
                          "className": "com.example.codetrails.orders.model.Order",
                          "methodName": "getMetadata()Ljava/util/Map;",
                          "methodNameOnly": "getMetadata",
                          "methodParams": [],
                          "qps": 48.440000000000005,
                          "qpm": 2906.4,
                          "counterValue": 9332.289999999999,
                          "errorRate": 0,
                          "latencyms": 0,
                          "errorRatePct": 0,
                          "httpRoute": null,
                          "httpMethod": null,
                          "cpuUtilizationPercent": 0,
                          "controllerMethod": false
                        },
                        "parentMpk": -758698648,
                        "children": {},
                        "mpk": -494301988
                      }
                    },
                    "mpk": -758698648
                  }
                },
                "mpk": 1251787835
              }
            },
            "mpk": -1048257232
          },
          "-1610030752": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -556059401,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getAmount()Ljava/lang/Double;",
              "methodNameOnly": "getAmount",
              "methodParams": [],
              "qps": 24.22,
              "qpm": 1453.2,
              "counterValue": 4666.87,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": -1610030752
          },
          "-1766119199": {
            "element": {
              "id": null,
              "domainName": "test",
              "serviceName": "codetrails",
              "methodDetailsHash": -712147848,
              "className": "com.example.codetrails.orders.model.Order",
              "methodName": "getCustomerId()Ljava/lang/String;",
              "methodNameOnly": "getCustomerId",
              "methodParams": [],
              "qps": 24.22,
              "qpm": 1453.2,
              "counterValue": 4666.87,
              "errorRate": 0,
              "latencyms": 0,
              "errorRatePct": 0,
              "httpRoute": null,
              "httpMethod": null,
              "cpuUtilizationPercent": 0,
              "controllerMethod": false
            },
            "parentMpk": -1280925096,
            "children": {},
            "mpk": -1766119199
          }
        },
        "mpk": -1280925096
      }
    },
    "mpk": 1559492060
  }
}




4. Get hot methods.

Request
curl -X 'GET' \
  'http://localhost:8081/test/api/method-graph-paths/hot-methods?serviceName=codetrails&cpuThreshold=1&step=1m' \
  -H 'accept: */*'

Response
[
  {
    "id": null,
    "domainName": "test",
    "serviceName": "codetrails",
    "methodDetailsHash": 33042171,
    "className": "com.example.codetrails.orders.service.impl.OrderServiceImpl",
    "methodName": "compareCharactersExpensively(CC)Z",
    "methodNameOnly": "compareCharactersExpensively",
    "methodParams": [
      "char",
      "char"
    ],
    "qps": 1723283.72,
    "qpm": 103397023.03,
    "counterValue": 642859750.25,
    "errorRate": 0,
    "latencyms": 0,
    "errorRatePct": 0,
    "httpRoute": null,
    "httpMethod": null,
    "cpuUtilizationPercent": 1.6107131273119877,
    "controllerMethod": false
  }
]

Returns a list of hot methods.



5. Find Service name
This is used to find the service name given a list of class names.
curl -X 'POST' \
  'http://localhost:8081/test/api/method-graph-paths/find-service-name' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "classNames": [
    "com.ckqa.service.PulsarProducerService",
    "com.ckqa.config.DwPulsarConfiguration",
    "com.ckqa.service.PulsarConsumerService"
]
}'

Response
{
  "available": true,
  "domainName": "test",
  "serviceNames": [
    "ns-pulsar-dropwizard-java-17"
  ]
}