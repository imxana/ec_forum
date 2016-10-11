normalError          = { 'code': '-10', 'codeState': 'something bad happended' }
safeError            = { 'code': '-11', 'codeState': 'unsafe attempt, who R U' }
requestError         = { 'code': '-12', 'codeState': 'method not allowed'      }
serverError          = { 'code': '-13', 'codeState': 'server error, maybe MySQL crashed' }


userNotExisted       = { 'code': '-20', 'codeState': 'user not existed'        }
usernameEmpty        = { 'code': '-21', 'codeState': 'username empty'          }
usernameExisted      = { 'code': '-22', 'codeState': 'username is existed'     }
usernameIllegal      = { 'code': '-23', 'codeState': 'username illegal'        }
useridEmpty          = { 'code': '-24', 'codeState': 'userid empty'            }
watchuserNotExisted  = { 'code': '-25', 'codeState': 'watch user not existed'  }
userAlreadyWatched   = { 'code': '-26', 'codeState': 'user already watched'    }
userAlreadyUnwatched = { 'code': '-27', 'codeState': 'user already unwatched'  }

pswEmpty             = { 'code': '-30', 'codeState': 'password empty'          }
pswWrong             = { 'code': '-31', 'codeState': 'wrong password'          }
pswIllegal           = { 'code': '-32', 'codeState': 'psw illegal'             }

emailNotExisted      = { 'code': '-40', 'codeState': 'email not existed'       }
emailEmpty           = { 'code': '-41', 'codeState': 'email empty'             }
emailExisted         = { 'code': '-42', 'codeState': 'email is existed'        }
emailIllegal         = { 'code': '-43', 'codeState': 'email illegal'           }
emailNotConfirmed    = { 'code': '-44', 'codeState': 'email not confirmed'     }
emailConfirmed       = { 'code': '-45', 'codeState': 'email confirmed already' }

loginNameNotExisted  = { 'code': '-50', 'codeState': 'login name not existed'  }
loginNameEmpty       = { 'code': '-51', 'codeState': 'login name empty'        }
loginNameIllegal     = { 'code': '-52', 'codeState': 'login name illegal'      }

articleTitleEmpty    = { 'code': '-60', 'codeState': 'article title empty'     }
articleTitleIllegal  = { 'code': '-61', 'codeState': 'article title illegal'   }
articleTextEmpty     = { 'code': '-62', 'codeState': 'article text empty'      }
articleNotExisted    = { 'code': '-63', 'codeState': 'article not existed'     }
articleidEmpty       = { 'code': '-64', 'codeState': 'article id empty'        }
articleAccess        = { 'code': '-65', 'codeState': 'have no access to do it' }

verifyEmpty          = { 'code': '-70', 'codeState': 'verify code empty'       }
verifyWrong          = { 'code': '-71', 'codeState': 'verify code wrong'       }
argsIllegal          = { 'code': '-72', 'codeState': 'illegal arguments value' }
argsEmpty            = { 'code': '-73', 'codeState': 'empty arguments value'   }

tagNotExisted        = { 'code': '-80', 'codeState': 'some tag not existed'    }
