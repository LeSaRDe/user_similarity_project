package usersimproj;

import java.util.*;
import java.lang.*;
import java.io.*;

import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.ling.*;

import it.uniroma1.lcl.babelfy.commons.*;
import it.uniroma1.lcl.babelfy.core.*;
import it.uniroma1.lcl.babelfy.commons.annotation.SemanticAnnotation;
import it.uniroma1.lcl.babelnet.*;
import it.uniroma1.lcl.jlt.util.Language;

class AnnotateUserText
{
    static public void main(String[] args)
    {
        try
        {
            UserTextIn uti = new UserTextIn(UserSimConstants.DB_PATH);
            String user_id = args[0];
            String t_start = args[1];
            String t_end = args[2];
            System.out.println("[DBG]: user_id  = " + user_id);
            System.out.println("[DBG]: t_start  = " + t_start);
            System.out.println("[DBG]: t_end  = " + t_end);
            uti.processUserTextFromDB(user_id, t_start, t_end);
            uti.allDone();
            System.out.println("[DBG]: " + user_id + " is done!");
        }
        catch(Exception e)
        {
            System.out.println("[ERR]: " + e.toString());
        } 
    }
}
