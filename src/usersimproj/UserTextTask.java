package usersimproj;

import java.io.*;
import java.util.*;
import java.sql.*;
import java.util.stream.*;

class UserTextTask implements Runnable
{
    private ArrayList<UserTextRec> m_ref_utrec = null;
    private Connection m_ref_db_conn = null;
    private UserTextRec m_in_utrec = null;

    public UserTextTask(Connection ref_db_conn, ArrayList<UserTextRec> ref_utrec, UserTextRec in_utrec)
    {
        m_ref_db_conn = ref_db_conn;
        m_ref_utrec = ref_utrec;
        m_in_utrec = in_utrec;
    }

    public void run()
    {
        CoreNLPWrap corenlp = new CoreNLPWrap(m_in_utrec.getcleantext(), true);
        corenlp.getDecomposedSentences();
        corenlp.getConstituentTrees();
        List<DeSentence> l_sentences = corenlp.getDeSentences();
        String sent_str = String.join("|", l_sentences.stream().map(desent->desent.toTaggedSentenceString()).collect(Collectors.toList()));
        String tree_str = String.join("|", l_sentences.stream().map(desent->desent.getPrunedTree(true).toString()).collect(Collectors.toList()));
        m_in_utrec.settaggedtext(sent_str);
        m_in_utrec.setparsetrees(tree_str);
        synchronized(m_ref_utrec)
        {
            m_ref_utrec.add(m_in_utrec);
        }
    }
}
