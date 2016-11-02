normalError          = { 'code': '-10', 'codeState': 'something bad happended' }
safeError            = { 'code': '-11', 'codeState': 'unsafe attempt, who R U' }
requestError         = { 'code': '-12', 'codeState': 'method not allowed'      }
serverError          = { 'code': '-13', 'codeState': 'server error, mostly the wrong sql syntax'}
methodAbort          = { 'code': '-14', 'codeState': 'method already aborted'  }

userNotExisted       = { 'code': '-20', 'codeState': 'user not existed'        }
usernameEmpty        = { 'code': '-21', 'codeState': 'username empty'          }
usernameExisted      = { 'code': '-22', 'codeState': 'username exists'     }
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
emailNotChanged      = { 'code': '-46', 'codeState': 'email not changed'       }

loginNameNotExisted  = { 'code': '-50', 'codeState': 'login name not existed'  }
loginNameEmpty       = { 'code': '-51', 'codeState': 'login name empty'        }
loginNameIllegal     = { 'code': '-52', 'codeState': 'login name illegal'      }

articleTitleEmpty    = { 'code': '-60', 'codeState': 'article title empty'     }
articleTitleIllegal  = { 'code': '-61', 'codeState': 'article title illegal'   }
articleTextEmpty     = { 'code': '-62', 'codeState': 'article text empty'      }
articleNotExisted    = { 'code': '-63', 'codeState': 'article not existed'     }
articleidEmpty       = { 'code': '-64', 'codeState': 'article id empty'        }
articleAccess        = { 'code': '-65', 'codeState': 'no access to del article'}
articleExist         = { 'code': '-66', 'codeState': 'article exists'          }
articleStarAlready   = { 'code': '-67', 'codeState': 'article star already'    }
articleNotStar       = { 'code': '-68', 'codeState': 'article not star'        }
articleRecommended   = { 'code': '-69', 'codeState': 'article recommend already'}
articleNotRecommend  = { 'code': '-6A', 'codeState': 'article not recommend'   }


verifyEmpty          = { 'code': '-70', 'codeState': 'verify code empty'       }
verifyWrong          = { 'code': '-71', 'codeState': 'verify code wrong'       }
argsIllegal          = { 'code': '-72', 'codeState': 'illegal arguments value' }
argsEmpty            = { 'code': '-73', 'codeState': 'empty arguments value'   }
tagNotExisted        = { 'code': '-74', 'codeState': 'some tag not existed'    }
tagNotIllegal        = { 'code': '-75', 'codeState': 'tags not illegal'        }

commentTextEmpty     = { 'code': '-80', 'codeState': 'comment text empty'      }
commentEventNotExsited={ 'code': '-81', 'codeState': 'comment event not exists '}
commentidEmpty       = { 'code': '-82', 'codeState': 'comment id empty'        }
commentNotExisted    = { 'code': '-83', 'codeState': 'comment not existed'     }
commentExsited       = { 'code': '-84', 'codeState': 'comment exists in event' }
commentAccess        = { 'code': '-85', 'codeState': 'no access to del comment'}

questionTitleEmpty   = { 'code': '-90', 'codeState': 'question title empty'     }
questionTitleIllegal = { 'code': '-91', 'codeState': 'question title illegal'   }
questionTextEmpty    = { 'code': '-92', 'codeState': 'question text empty'      }
questionNotExisted   = { 'code': '-93', 'codeState': 'question not existed'     }
questionidEmpty      = { 'code': '-94', 'codeState': 'question id empty'        }
questionAccess       = { 'code': '-95', 'codeState': 'no access to del question'}
questionExist        = { 'code': '-96', 'codeState': 'question exists'          }
questionStarAlready  = { 'code': '-97', 'codeState': 'question star already'    }
questionNotStar      = { 'code': '-98', 'codeState': 'question not star'        }
questionLikeAlready  = { 'code': '-99', 'codeState': 'question like already'    }
questionNotLike      = { 'code': '-9A', 'codeState': 'question not like'        }
questionDislikeAlready={ 'code': '-9B', 'codeState': 'question dislike already' }
questionNotDislike   = { 'code': '-9C', 'codeState': 'question not dislike'     }
questionSelfAction   = { 'code': '-9D', 'codeState': 'question self action'     }







