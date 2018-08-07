package usersimproj;

import java.util.*;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.io.File;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.*;
import java.lang.StringBuffer;
import java.lang.Exception;
import java.util.regex.*;

import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.trees.*;


public class CoreNLPWrap
{
    /**
     * Class Members
     */
    // properties for CoreNLP pipeline
    private Properties m_props;
    // path for the stopword file
    private final String m_swfilepath = "/home/fcmeng/user_similarity_project/res/stopwords.txt";
    // stopword array
    //private String[] m_a_stopwords;
    // CoreNLP pipeline instance
    private StanfordCoreNLP m_pipeline;
    // sentences parsed from the input text
    private List<CoreSentence> m_sentences;
    // output sentenses
    private List<DeSentence> m_desentences;
    // switch for online/offline run
    // true -- online
    private boolean m_online;
    // CoreNLP client for online mode only
    private StanfordCoreNLPClient m_client;

    /**
     * Class Methods
     */
    // constructor
    // the stopword annotator is not a built-in one. instead, it is introduced 
    // from an opensource extension of CoreNLP. 
    // the reference is as follows:
    // https://github.com/plandes/stopword-annotator
    /**
     * NOTE:
     * The stopword annotator so far is not working perfecting in the C/S mode,
     * something needs to be serialized.
     * Temporarily I remove it from the CoreNLP server. Also, since it would not 
     * be necessary to take stopwords into accound when annotating sentences, not
     * even necessary for parsing, it won't hurt anything running without it. 
     * Instead, when pruning parse trees, we DO need to get rid of stopwords.
     * Lets do that as an individual job. 
     */
    public CoreNLPWrap(String in_txt, boolean online)
    {
        CoreDocument coredoc;
        m_props = new Properties();
        m_props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse");
        if(!online)
        {
            /*
            m_props.setProperty("customAnnotatorClass.stopword", "usersimproj.StopwordAnnotator");
            try
            {
                m_props.setProperty("StopwordAnnotator.STOPWORDS_LIST", loadStopwordList(m_swfilepath));
            }
            catch(Exception e)
            {
                e.toString();
                e.printStackTrace();
            }
            */
            m_pipeline = new StanfordCoreNLP(m_props);
            coredoc = new CoreDocument(in_txt);
            m_pipeline.annotate(coredoc);
        }
        else
        {
            m_client = new StanfordCoreNLPClient(m_props, 
                UserSimConstants.CORENLP_SERV_HOSTNAME, 
                UserSimConstants.CORENLP_SERV_PORT,
                UserSimConstants.CORENLP_CLIENT_THREAD);
            //System.out.println("[DBG]: CoreNLPWrap in_txt = " + in_txt);
            Annotation annodoc = new Annotation(in_txt);
            //System.out.println("[DBG]: CoreNLPWrap annotation1");
            m_client.annotate(annodoc);
            //System.out.println("[DBG]: CoreNLPWrap annotation2");
            coredoc = new CoreDocument(annodoc);
        }
        m_sentences = coredoc.sentences();
        m_desentences = new ArrayList<DeSentence>();
        for(CoreSentence sent : m_sentences)
        {
            m_desentences.add(new DeSentence(sent.text()));
        }
    };

    // reads stopwords from a file, and outputs a sorted string array 
    /*
    private String[] loadStopwordList(String swfilepath)
    {
        String [] ret = null;
        try
        {
            File swfile = new File(swfilepath);
            ArrayList<String> swstrbf = new ArrayList<String>();
            BufferedReader bfread = new BufferedReader(new InputStreamReader(new FileInputStream(swfile), "UTF-8"));
            String ln;
            while((ln = bfread.readLine()) != null)
            {
                swstrbf.add(ln);
            }
            ret = swstrbf.toArray(new String[swstrbf.size()]);
        }
        catch(Exception e)
        {
            System.out.println("[ERR]: loadStopwordList " + e.toString());
        }
        Arrays.sort(ret);
        return ret;
    }
    */

    public List<DeSentence> getDeSentences()
    {
        return m_desentences;
    }

    // decompose sentences
    public boolean getDecomposedSentences()
    {
        boolean ret = true;
        if(m_sentences == null || m_desentences == null)
        {
            return false;
        }
        for(DeSentence desent : m_desentences)
        {
            CoreSentence coresent = m_sentences.get(m_desentences.indexOf(desent));
            if(coresent == null)
            {
                System.out.println("[ERR]: " + "DeSentence->CoreSentence fails!");
                ret = false;
                continue;
            }
            for(CoreLabel token : coresent.tokens())
            {
                if(!desent.appendToken(new DeToken(token.word(), token.tag(), token.ner(), token.lemma())))
                {
                    System.out.println("[ERR]: " + "something wrong happened when adding token to DeSentence!");
                }
            }
        }
        return ret;
    }

    /*
    private DeSentence decomposeSentence(CoreSentence sentence)
    {
        if(sentence == null)
        {
            return null;
        }
        DeSentence ret = new DeSentence(sentence.text());
        for(CoreLabel token : sentence.tokens())
        {
            if(!ret.appendToken(new DeToken(token.word(), token.tag(), token.ner(), token.lemma())))
            {
                System.out.println("[ERR]: " + "something wrong happened when adding token to DeSentence!");
            }
        }
        return ret;
    }
    */

    // compute constituency-based parse trees
    public boolean getConstituentTrees()
    {
        boolean ret = true;
        if(m_sentences == null || m_desentences == null)
        {
            return false;
        }
        for(DeSentence desent : m_desentences)
        {
            desent.setConstituentTree(m_sentences.get(m_desentences.indexOf(desent)).constituencyParse());
        }
        return ret;
    }

/*
    // this function reads in a constituency-based parse tree, and converts it
    // to a flat tree string, e.g. (S (NP I#12345678) (VP (V saw#23456789) (NP him#34567890))).
    public StringBuilder getOneTreeString(Tree c_tree, StringBuilder strbldr)
    {
        // if the root of c_tree is a leaf,
        // then directly returns the word at this leaf
        // and its sense offset.
        if(c_tree.isLeaf())
        {
            strbldr.append(c_tree.value());
            //System.out.print(c_tree.value());
            return strbldr;
        }
        // if c_tree is still a subtree, then we recursively print it.
        else
        {
            // every tree needs start with '('
            strbldr.append("(");
            //System.out.print("(");
            // then it is followed with the POS tag of the root of c_tree
            strbldr.append(c_tree.value() + " ");
            //System.out.print(c_tree.value() + " ");
            // then we do recursions over all subtrees in c_tree
            // it actually is a depth-first traversal
            List<Tree> l_tr = c_tree.getChildrenAsList();
            for(Tree subtree : l_tr)
            {
                printTree(subtree, strbldr);
                if(l_tr.indexOf(subtree) != (l_tr.size()-1))
                {
                    strbldr.append(" ");
                    //System.out.print(" ");
                }
            }
            // when all subtrees are done, we put ')' at the end
            strbldr.append(")");
            //System.out.print(")");
            return strbldr;
        }
    }
*/
    public void shutdownCoreNLPClient()
    {
        if(m_online)
        {
            try
            {
                m_client.shutdown();
            }
            catch(Exception e)
            {
                System.out.println("[ERR]: Failed when shutting down CoreNLP client!");
            }
        }
    }
}
