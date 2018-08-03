package usersimproj;

import java.io.*;
import java.util.*;
import java.sql.*;
import java.util.stream.*;

class UserTextTask implements Runnable
{
    private Connection m_ref_db_conn = null;
    private UserTextRec m_in_utrec = null;
    private UserTextIn m_utin = null;

    public UserTextTask(UserTextIn utin, Connection ref_db_conn, UserTextRec in_utrec)
    {
        m_utin = utin;
        m_ref_db_conn = ref_db_conn;
        m_in_utrec = in_utrec;
    }

    public void run()
    {
        //System.out.println("[DBG]: UserTextTask run...");
        CoreNLPWrap corenlp = new CoreNLPWrap(m_in_utrec.getcleantext(), true);
        corenlp.getDecomposedSentences();
        corenlp.getConstituentTrees();
        List<DeSentence> l_sentences = corenlp.getDeSentences();
        BabelWrap bw = new BabelWrap();
        for(DeSentence sent : l_sentences)
        {
            bw.getSynsets(sent);
        }
        String sent_str = String.join("|", l_sentences.stream().map(desent->desent.toTaggedSentenceString()).collect(Collectors.toList()));
        String tree_str = String.join("|", l_sentences.stream().map(desent->desent.getPrunedTree(true).toString()).collect(Collectors.toList()));
        //System.out.println("[DBG]: parse_trees = " + tree_str);
        m_in_utrec.settaggedtext(sent_str);
        m_in_utrec.setparsetrees(tree_str);
        m_utin.addUpdatedUserTextRec(m_in_utrec);
        //System.out.println("[DBG]: UserTextTask one record ready!");
    }
}
