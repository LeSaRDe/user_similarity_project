package usersimproj;

import java.io.*;
import java.util.*;
import java.sql.*;
import java.util.concurrent.*;

import org.json.simple.*;
import org.json.simple.parser.*


class UserTextIn
{
    /**
     * Class Constants
     */
    public final int MAX_CACHED 5000;

    /**
     * Class Members
     */
    private Connection m_db_conn = null;;
    private ArrayList<UserTextRec> m_l_utrec = null; 
    private ExecutorService m_pool;


    /**
     * Class Methods
     */
    // for database input
    public UserTextIn(String db_conn_str)
    {
        try
        {
            m_db_conn = DriverManager.getConnection(db_conn_str);
            m_db_conn.setAutoCommit(false);
        }
        catch(Exception e)
        {
            System.out.println("[ERR]: " + e.toString());
        }
        m_l_utrec = new ArrayList<UserTextRec>();
        m_pool = Executors.newCachedThreadPool();
    }

    public void shutdownDB()
    {
        if (m_db_conn != null)
        {
            try
            {
                m_db_conn.close();
            }
            catch(Exception)
            {
                System.out.println("[ERR]: " + e.toString());
            }
        }
    }

    // this function fetches user text for a given user within a certian time range
    public String fetchUserTextFromDB(String user_id, String time_s, String time_e) 
    {
        String query_str = null;
        if(time_s == null || time_e == null)
        {
            query_str = String.format("SELECT user_id, time, clean_text FROM tb_user_text_full WHERE (user_id = '%s')", user_id);
        }
        else
        {
            query_str = String.format("SELECT user_id, time, clean_text FROM tb_user_text_full WHERE (user_id = '%s') AND (time BETWEEN '%s' AND '%s')", 
                                        user_id, time_s, time_e);
        }
        try
        (
            Statement st = m_db_conn.createStatement();
            ResultSet rs = st.executeQuery(query_str);
        )
        {
            while(rs.next())
            {
                m_pool.execute(new UserTextTask(m_db_conn, m_l_utrec, 
                                new UserTextRec(rs.getString("user_id"), rs.getString("time"), rs.getString("clean_text"), null, null)));
                commitUserTextRecs(MAX_CACHED);
            }
        }
        catch(Exception e)
        {
            System.out.println("[ERR]: " + e.toString());
        }
    }

    private void commitUserTextRecs(int max_cached)
    {
        synchronized(m_l_utrec)
        {
            if(m_l_utrec.size() > max_cached)
            {
                ArrayList<Integer> l_rm = new ArrayList<Integer>();
                String update_str = null;
                for(UserTextRec utc : m_l_utrec)
                {
                    update_str = "UPDATE tb_user_text_full SET tagged_text = ? , parse_trees = ? WHERE user_id = ?, time = ?";
                    try
                    (
                       PreparedStatement st = m_db_conn.prepareStatement(update_str); 
                    )
                    {
                        st.setString(1, utc.gettaggedtext());
                        st.setString(2, utc.getparsetrees());
                        st.setString(3, utc.getuserid());
                        st.setString(4, utc.gettime());
                        st.executeUpdate();
                    }
                    catch(Exception e)
                    {
                        System.out.println("[ERR]: " + e.toString());
                    }

                    l_rm.add(m_l_utrec.indexOf(utc));
                }
                m_db_conn.commit();

                Set<Integer> hs = new HashSet<Integer>();
                hs.addAll(l_rm);
                l_rm.clear();
                l_rm.addAll(hs);

                for(Integer i_rm : l_rm)
                {
                    m_l_utrec.remove(i_rm.intValue());
                }
            }
        }
    }
}
